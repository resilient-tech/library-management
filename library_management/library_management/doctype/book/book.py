# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


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

	pass
