# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibrarySettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from library_management.library_management.doctype.library_hours.library_hours import LibraryHours

		auto_extend_enabled: DF.Check
		default_issue_period: DF.Int
		email_notifications: DF.Check
		enable_reservations: DF.Check
		fine_per_day: DF.Currency
		library_hours: DF.Table[LibraryHours]
		library_name: DF.Data
		max_books_per_member: DF.Int
		membership_fees: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.validate_fees_fine_rates()
		self.validate_issue_periods()

	def validate_fees_fine_rates(self):
		if hasattr(self, "membership_fees") and self.membership_fees < 0:
			frappe.throw("Membership fees cannot be negative")

		if hasattr(self, "fine_per_day") and self.fine_per_day < 0:
			frappe.throw("Fine per day cannot be negative")

	def validate_issue_periods(self):
		if hasattr(self, "default_issue_period") and self.default_issue_period <= 0:
			frappe.throw("Default issue period must be greater than 0 days")
