# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate

from library_management.library_management.doctype.book_transaction.book_transaction import (
	get_issued_book_count,
	get_total_fines,
)


class LibraryMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from library_management.library_management.doctype.member_preferences.member_preferences import (
			MemberPreferences,
		)

		access_level: DF.Literal["Basic", "Premium", "VIP"]
		address: DF.Text | None
		current_books_issued: DF.Int
		date_of_birth: DF.Date | None
		email: DF.Data | None
		emergency_name: DF.Data | None
		emergency_phone: DF.Data | None
		first_name: DF.Data
		last_name: DF.Data
		max_books_allowed: DF.Int
		member_type: DF.Literal["Student", "Faculty", "Staff", "External"]
		membership_end_date: DF.Date | None
		membership_start_date: DF.Date | None
		membership_status: DF.Literal["Active", "Suspended", "Expired", "Cancelled"]
		naming_series: DF.Literal["MEM-.YYYY.-.#####"]
		phone: DF.Data | None
		preferences: DF.Table[MemberPreferences]
		profile_picture: DF.AttachImage | None
		total_fines: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.update_issued_books_count()
		self.update_total_fines()

	def before_insert(self):
		if not self.membership_start_date:
			self.membership_start_date = nowdate()

		if not self.membership_end_date:
			# Default to 1 year membership
			self.membership_end_date = add_days(self.membership_start_date, 365)

	def update_issued_books_count(self):
		self.current_books_issued = get_issued_book_count(member=self.name)

	def update_total_fines(self):
		self.total_fines = get_total_fines(member=self.name)

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"
