# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, getdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Transaction ID"),
			"fieldname": "transaction_id",
			"fieldtype": "Link",
			"options": "Book Transaction",
			"width": 120,
		},
		{
			"label": _("Member ID"),
			"fieldname": "member",
			"fieldtype": "Link",
			"options": "Library Member",
			"width": 120,
		},
		{
			"label": _("Member Name"),
			"fieldname": "member_name",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Book ID"),
			"fieldname": "book",
			"fieldtype": "Link",
			"options": "Book",
			"width": 120,
		},
		{
			"label": _("Book Title"),
			"fieldname": "book_title",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("ISBN"),
			"fieldname": "isbn",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Issue Date"),
			"fieldname": "transaction_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Days Overdue"),
			"fieldname": "days_overdue",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Fine Amount"),
			"fieldname": "fine_amount",
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Issued By"),
			"fieldname": "issued_by",
			"fieldtype": "Link",
			"options": "User",
			"width": 120,
		},
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 120,
		},
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql(
		f"""
		SELECT
			bt.name as transaction_id,
			bt.member,
			CONCAT(lm.first_name, ' ', lm.last_name) as member_name,
			bt.book,
			b.title as book_title,
			b.isbn,
			DATE(bt.transaction_date) as transaction_date,
			bt.due_date,
			bt.fine_amount,
			bt.issued_by,
			ll.location_name as location
		FROM `tabBook Transaction` bt
		JOIN `tabLibrary Member` lm ON bt.member = lm.name
		JOIN `tabBook` b ON bt.book = b.name
		LEFT JOIN `tabLibrary Location` ll ON b.location = ll.name
		WHERE bt.transaction_type = 'Issue'
			AND bt.docstatus = 1
			AND bt.return_date IS NULL
			{conditions}
		ORDER BY bt.due_date ASC, bt.transaction_date DESC
		""",
		filters,
		as_dict=1,
	)

	# Calculate days overdue and status for each record
	today = getdate()
	for row in data:
		if row.due_date:
			days_overdue = date_diff(today, row.due_date)
			row.days_overdue = max(0, days_overdue)

			if days_overdue > 0:
				row.status = f"Overdue ({days_overdue} days)"
			elif days_overdue > -7:  # Due within a week
				row.status = f"Due Soon ({abs(days_overdue)} days)"
			else:
				row.status = "Active"
		else:
			row.days_overdue = 0
			row.status = "Active"

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("member"):
		conditions += " AND bt.member = %(member)s"

	if filters.get("book"):
		conditions += " AND bt.book = %(book)s"

	if filters.get("from_date"):
		conditions += " AND DATE(bt.transaction_date) >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND DATE(bt.transaction_date) <= %(to_date)s"

	if filters.get("status"):
		if filters.get("status") == "Overdue":
			conditions += " AND bt.due_date < CURDATE()"
		elif filters.get("status") == "Due Soon":
			conditions += " AND bt.due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
		elif filters.get("status") == "Active":
			conditions += " AND bt.due_date > DATE_ADD(CURDATE(), INTERVAL 7 DAY)"

	return conditions


@frappe.whitelist()
def send_reminder_emails(transactions):
	"""Send reminder emails to members for selected transactions"""
	sent_count = 0

	for transaction_id in transactions:
		try:
			transaction_doc = frappe.get_doc("Book Transaction", transaction_id)
			member_doc = frappe.get_doc("Library Member", transaction_doc.member)
			book_doc = frappe.get_doc("Book", transaction_doc.book)

			if member_doc.email:
				# Send email using Frappe's email system
				frappe.sendmail(
					recipients=[member_doc.email],
					subject=_("Reminder: Book Return Due - {0}").format(book_doc.title),
					template="book_return_reminder",
					args={
						"member_name": f"{member_doc.first_name} {member_doc.last_name}",
						"book_title": book_doc.title,
						"due_date": transaction_doc.due_date,
						"transaction_id": transaction_doc.name,
						"days_overdue": max(0, date_diff(getdate(), transaction_doc.due_date)),
					},
					now=True,
				)
				sent_count += 1

		except Exception as e:
			frappe.log_error(f"Error sending reminder email for {transaction_id}: {e!s}")
			continue

	return {"sent_count": sent_count}


@frappe.whitelist()
def bulk_return_books(transactions):
	"""Bulk return books for selected transactions"""
	returned_count = 0

	for transaction_id in transactions:
		try:
			transaction_doc = frappe.get_doc("Book Transaction", transaction_id)

			# Validate that book can be returned
			if transaction_doc.return_date:
				continue  # Already returned

			# Set return date and calculate fine if overdue
			transaction_doc.return_date = getdate()
			transaction_doc.transaction_type = "Return"
			transaction_doc.calculate_fine()
			transaction_doc.set_returned_to()

			# Save the transaction
			transaction_doc.save(ignore_permissions=True)
			transaction_doc.submit()

			returned_count += 1

		except Exception as e:
			frappe.log_error(f"Error returning book for {transaction_id}: {e!s}")
			continue

	return {"returned_count": returned_count}


@frappe.whitelist()
def generate_fine_report(transactions):
	"""Generate a fine collection report for overdue transactions"""
	try:
		# Create a temporary report with fine details
		fine_data = []
		total_fines = 0

		for transaction_id in transactions:
			transaction_doc = frappe.get_doc("Book Transaction", transaction_id)
			member_doc = frappe.get_doc("Library Member", transaction_doc.member)
			book_doc = frappe.get_doc("Book", transaction_doc.book)

			if transaction_doc.due_date and getdate() > getdate(transaction_doc.due_date):
				overdue_days = date_diff(getdate(), transaction_doc.due_date)
				settings = frappe.get_single("Library Settings")
				fine_amount = overdue_days * settings.fine_per_day

				fine_data.append(
					{
						"transaction_id": transaction_doc.name,
						"member": f"{member_doc.first_name} {member_doc.last_name}",
						"member_id": member_doc.name,
						"book_title": book_doc.title,
						"due_date": transaction_doc.due_date,
						"overdue_days": overdue_days,
						"fine_amount": fine_amount,
					}
				)
				total_fines += fine_amount

		# You could create a PDF report or redirect to a fine collection form
		# For now, we'll return a success message with summary
		return {
			"success": True,
			"total_transactions": len(fine_data),
			"total_fine_amount": total_fines,
			"report_url": f"/app/query-report/Fine Collection Report?transaction_ids={','.join(transactions)}",
		}

	except Exception as e:
		frappe.log_error(f"Error generating fine report: {e!s}")
		frappe.throw(_("Error generating fine report. Please check the error logs."))
