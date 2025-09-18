// Copyright (c) 2025, Library Management and contributors
// For license information, please see license.txt

frappe.query_reports["Issued Books Report"] = {
	filters: [
		{
			fieldname: "member",
			label: __("Member"),
			fieldtype: "Link",
			options: "Library Member",
		},
		{
			fieldname: "book",
			label: __("Book"),
			fieldtype: "Link",
			options: "Book",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Overdue", "Due Soon", "Active"],
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "status") {
			if (data && data.status) {
				if (data.status.includes("Overdue")) {
					value = `<span style="color: red; font-weight: bold;">${data.status}</span>`;
				} else if (data.status.includes("Due Soon")) {
					value = `<span style="color: orange; font-weight: bold;">${data.status}</span>`;
				} else {
					value = `<span style="color: green;">${data.status}</span>`;
				}
			}
		}

		if (column.fieldname == "days_overdue" && data && data.days_overdue > 0) {
			value = `<span style="color: red; font-weight: bold;">${data.days_overdue}</span>`;
		}

		if (column.fieldname == "fine_amount" && data && data.fine_amount > 0) {
			value = `<span style="color: red; font-weight: bold;">${value}</span>`;
		}

		return value;
	},

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload: function (report) {
		// Add custom buttons to the report
		report.page.add_inner_button(__("Send Reminder Email"), function () {
			let selected_items = report.get_checked_items();

			if (selected_items.length === 0) {
				frappe.msgprint(__("Please select at least one transaction to send reminders."));
				return;
			}

			frappe.confirm(
				__("Send reminder emails to {0} member(s)?", [selected_items.length]),
				function () {
					frappe.call({
						method: "library_management.library_management.report.issued_books_report.issued_books_report.send_reminder_emails",
						args: {
							transactions: selected_items.map((item) => item.transaction_id),
						},
						callback: function (r) {
							if (r.message) {
								frappe.msgprint(
									__("Reminder emails sent successfully to {0} member(s)", [
										r.message.sent_count,
									])
								);
							}
						},
					});
				}
			);
		});

		report.page.add_inner_button(__("Bulk Return Books"), function () {
			let selected_items = report.get_checked_items();

			if (selected_items.length === 0) {
				frappe.msgprint(__("Please select at least one transaction to return books."));
				return;
			}

			// Filter only active transactions (not overdue requiring fine collection)
			let returnable_items = selected_items.filter(
				(item) => !item.status.includes("Overdue")
			);

			if (returnable_items.length === 0) {
				frappe.msgprint(
					__(
						"Selected transactions have overdue fines. Please collect fines before returning."
					)
				);
				return;
			}

			frappe.confirm(
				__("Return {0} book(s)? This action cannot be undone.", [returnable_items.length]),
				function () {
					frappe.call({
						method: "library_management.library_management.report.issued_books_report.issued_books_report.bulk_return_books",
						args: {
							transactions: returnable_items.map((item) => item.transaction_id),
						},
						callback: function (r) {
							if (r.message) {
								frappe.msgprint(
									__("Successfully returned {0} book(s)", [
										r.message.returned_count,
									])
								);
								report.refresh();
							}
						},
					});
				}
			);
		});

		report.page.add_inner_button(__("Generate Fine Report"), function () {
			let selected_items = report.get_checked_items();

			if (selected_items.length === 0) {
				frappe.msgprint(__("Please select transactions to generate fine report."));
				return;
			}

			// Filter overdue items only
			let overdue_items = selected_items.filter((item) => item.status.includes("Overdue"));

			if (overdue_items.length === 0) {
				frappe.msgprint(__("No overdue transactions selected."));
				return;
			}

			frappe.call({
				method: "library_management.library_management.report.issued_books_report.issued_books_report.generate_fine_report",
				args: {
					transactions: overdue_items.map((item) => item.transaction_id),
				},
				callback: function (r) {
					if (r.message && r.message.report_url) {
						window.open(r.message.report_url, "_blank");
					}
				},
			});
		});

		report.page.add_inner_button(__("Export Selected"), function () {
			let selected_items = report.get_checked_items();

			if (selected_items.length === 0) {
				frappe.msgprint(__("Please select items to export."));
				return;
			}

			// Convert selected items to CSV and download
			let csv_data = report.convert_to_csv(selected_items);
			let filename = `issued_books_${frappe.datetime.get_today()}.csv`;

			frappe.tools.downloadify(csv_data, null, filename);
			frappe.msgprint(__("Export completed: {0} records", [selected_items.length]));
		});
	},

	convert_to_csv: function (data) {
		if (!data || data.length === 0) return "";

		// Get headers from first row
		let headers = Object.keys(data[0]);
		let csv = headers.join(",") + "\n";

		// Add data rows
		data.forEach((row) => {
			let values = headers.map((header) => {
				let value = row[header] || "";
				// Escape quotes and wrap in quotes if contains comma
				if (typeof value === "string" && (value.includes(",") || value.includes('"'))) {
					value = '"' + value.replace(/"/g, '""') + '"';
				}
				return value;
			});
			csv += values.join(",") + "\n";
		});

		return csv;
	},
};
