# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from library_management.library_management.doctype.book_transaction.book_transaction import (
	get_issued_book_count,
)


class Book(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from library_management.library_management.doctype.book_author.book_author import BookAuthor

		acquisition_date: DF.Date | None
		authors: DF.Table[BookAuthor]
		available_copies: DF.Int
		average_rating: DF.Float
		book_category: DF.Link | None
		book_cover: DF.AttachImage | None
		condition: DF.Literal["New", "Good", "Fair", "Poor"]
		description: DF.TextEditor | None
		digital_copy_available: DF.Check
		digital_file: DF.Attach | None
		edition: DF.Data | None
		is_reference_only: DF.Check
		isbn: DF.Data | None
		language: DF.Link | None
		location: DF.Link | None
		naming_series: DF.Literal["LIB-BOOK-.#####"]
		popularity_score: DF.Float
		price: DF.Currency
		publication_date: DF.Date | None
		publisher: DF.Link | None
		rack_number: DF.Data | None
		subcategory: DF.Link | None
		subtitle: DF.Data | None
		tags: DF.Data | None
		title: DF.Data
		total_copies: DF.Int
		total_ratings: DF.Int
	# end: auto-generated types

	def validate(self):
		self.validate_authors()
		self.validate_total_copies()
		self.update_available_copies()

	def validate_authors(self):
		if not self.authors:
			frappe.throw("At least one author is required")

		total_contribution = sum(author.contribution_percentage or 0 for author in self.authors)
		if total_contribution != 100:
			frappe.throw(f"Total author contribution must be 100%. Current: {total_contribution}%")

		# Check for duplicate authors
		author_names = [author.author for author in self.authors]
		if len(author_names) != len(set(author_names)):
			frappe.throw("Duplicate authors are not allowed")

	def validate_total_copies(self):
		if self.total_copies <= 0:
			frappe.throw("Total copies must be greater than 0")

	def update_available_copies(self):
		if self.is_new():
			self.available_copies = self.total_copies
			return

		issued_count = get_issued_book_count(book=self.name)
		self.available_copies = self.total_copies - issued_count

	@frappe.whitelist()
	def get_current_issues(self):
		return frappe.get_all(
			"Book Transaction",
			{
				"book": self.name,
				"transaction_type": "Issue",
				"docstatus": 1,
				"return_date": ["is", "not set"],
			},
			["name", "member", "transaction_date", "due_date"],
		)

	def is_available(self):
		return self.available_copies > 0 and not self.is_reference_only
