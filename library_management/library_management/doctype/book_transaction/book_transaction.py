# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.query_builder.functions import Coalesce, Sum
from frappe.utils import add_days, date_diff, getdate, now_datetime, nowdate


class BookTransaction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		auto_extended: DF.Check
		book: DF.Link
		condition_on_issue: DF.Literal["New", "Good", "Fair", "Poor"]
		condition_on_return: DF.Literal["New", "Good", "Fair", "Poor"]
		due_date: DF.Date | None
		fine_amount: DF.Currency
		fine_paid: DF.Check
		issued_by: DF.Link | None
		member: DF.Link
		naming_series: DF.Literal["TXN-.#####"]
		notes: DF.Text | None
		renewed_count: DF.Int
		return_date: DF.Date | None
		returned_to: DF.Link | None
		transaction_date: DF.Datetime | None
		transaction_type: DF.Literal["Issue", "Return", "Reserve"]
	# end: auto-generated types

	# TODO
	# Analyze existing methods
	# Discuss scope of improvements
	# setup their controller methods
	# Create workflow actions from the methods

	def validate_member_status(self):
		member_doc = frappe.get_doc("Library Member", self.member)

		if member_doc.membership_status != "Active":
			frappe.throw(
				_("Member {0} is not active. Current status: {1}").format(
					self.member, member_doc.membership_status
				)
			)

		# Check if membership has expired
		if getdate(member_doc.membership_end_date) < getdate():
			frappe.throw(
				_("Member {0} membership has expired on {1}").format(
					self.member, member_doc.membership_end_date
				)
			)

	def validate_book_availability(self):
		if self.transaction_type == "Issue":
			book_doc = frappe.get_doc("Book", self.book)

			if book_doc.is_reference_only:
				frappe.throw(_("Book {0} is reference only and cannot be issued").format(self.book))

			# Use the Book's method to check availability
			if not book_doc.is_available():
				frappe.throw(_("Book {0} is not available. All copies are issued").format(self.book))

	def validate_issue_limits(self):
		member_doc = frappe.get_doc("Library Member", self.member)

		if member_doc.current_books_issued >= member_doc.max_books_allowed:
			frappe.throw(
				_("Member {0} has reached maximum book issue limit of {1}").format(
					self.member, member_doc.max_books_allowed
				)
			)

		# Check for unpaid fines
		if member_doc.total_fines > 0:
			frappe.throw(
				_(
					"Member {0} has outstanding fines of {1}. Please clear fines before issuing new books"
				).format(self.member, member_doc.total_fines)
			)

	def set_default_values(self):
		if not self.transaction_date:
			self.transaction_date = now_datetime()

		if self.transaction_type == "Issue" and not self.due_date:
			settings = frappe.get_single("Library Settings")
			default_period = settings.default_issue_period
			self.due_date = add_days(getdate(self.transaction_date), default_period)

		if self.transaction_type == "Return" and not self.return_date:
			self.return_date = getdate()

	def calculate_fine(self):
		if self.transaction_type == "Return" and self.due_date and self.return_date:
			if getdate(self.return_date) > getdate(self.due_date):
				settings = frappe.get_single("Library Settings")
				fine_per_day = settings.fine_per_day

				overdue_days = date_diff(self.return_date, self.due_date)
				self.fine_amount = overdue_days * fine_per_day

	def set_issued_by(self):
		if not self.issued_by:
			self.issued_by = frappe.session.user

	def set_returned_to(self):
		if not self.returned_to:
			self.returned_to = frappe.session.user

	def update_book_availability(self):
		book_doc = frappe.get_doc("Book", self.book)
		book_doc.update_available_copies()
		book_doc.save(ignore_permissions=True)

	def update_member_statistics(self):
		member_doc = frappe.get_doc("Library Member", self.member)
		member_doc.update_issued_books_count()
		member_doc.update_total_fines()
		member_doc.save(ignore_permissions=True)


def get_issued_book_count(member=None, book=None):
	filters = {
		"transaction_type": "Issue",
		"docstatus": 1,
		"return_date": ["is", "not set"],
	}

	if member:
		filters["member"] = member

	if book:
		filters["book"] = book

	return frappe.db.count("Book Transaction", filters)


def get_total_fines(member):
	transaction = frappe.qb.DocType("Book Transaction")

	total_fines = (
		frappe.qb.from_(transaction)
		.select(Coalesce(Sum(transaction.fine_amount), 0))
		.where((transaction.member == member) & (transaction.docstatus == 1) & (transaction.fine_paid == 0))
		.run()
	)[0][0]

	return total_fines
