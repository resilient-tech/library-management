# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, date_diff, getdate, now_datetime
from frappe import _


class BookTransaction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		auto_extended: DF.Check
		barcode_scanned: DF.Check
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
		transaction_type: DF.Literal["Issue", "Return", "Renew", "Reserve"]
	# end: auto-generated types
	pass
