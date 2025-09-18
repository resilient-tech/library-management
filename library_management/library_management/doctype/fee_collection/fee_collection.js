// Fee Collection Client Script
// This script provides interactive functionality for the Fee Collection doctype

frappe.ui.form.on("Fee Collection", {
	refresh: function (frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 0 && frm.doc.member) {
			frm.add_custom_button(__("Load Outstanding Fines"), function () {
				frm.call("load_outstanding_fines").then(() => {
					frm.refresh_field("fine_details");
					frm.refresh_field("fine_amount");
					frm.refresh_field("total_amount");
					frm.refresh_field("net_amount");
				});
			});
		}

		// Print receipt button
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Print Receipt"), function () {
				frappe.route_options = { name: frm.doc.name };
				frappe.set_route("print", "Fee Collection", frm.doc.name);
			});
		}
	},

	member: function (frm) {
		// Clear fine details when member changes
		if (frm.doc.member) {
			frm.set_value("fine_details", []);
			frm.refresh_field("fine_details");
		}
	},

	membership_fee: function (frm) {
		calculate_total_amount(frm);
	},

	late_fee: function (frm) {
		calculate_total_amount(frm);
	},

	damage_fee: function (frm) {
		calculate_total_amount(frm);
	},

	other_fee: function (frm) {
		calculate_total_amount(frm);
	},

	fine_amount: function (frm) {
		calculate_total_amount(frm);
	},

	discount_amount: function (frm) {
		calculate_total_amount(frm);
	},
});

function calculate_total_amount(frm) {
	var total =
		(frm.doc.membership_fee || 0) +
		(frm.doc.late_fee || 0) +
		(frm.doc.damage_fee || 0) +
		(frm.doc.other_fee || 0) +
		(frm.doc.fine_amount || 0);

	frm.set_value("total_amount", total);
	frm.set_value("net_amount", total - (frm.doc.discount_amount || 0));
}

// Child table events
frappe.ui.form.on("Fee Collection Fine Detail", {
	fine_details_add: function (frm, cdt, cdn) {
		// Auto-calculate fine amount when new row is added
		calculate_fine_total(frm);
	},

	fine_details_remove: function (frm) {
		// Recalculate when row is removed
		calculate_fine_total(frm);
	},
});

function calculate_fine_total(frm) {
	var total_fine = 0;
	frm.doc.fine_details.forEach(function (row) {
		total_fine += row.fine_amount || 0;
	});

	frm.set_value("fine_amount", total_fine);
	calculate_total_amount(frm);
}
