# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FeeCollectionFineDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		book: DF.Link | None
		due_date: DF.Date | None
		fine_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		return_date: DF.Date | None
		transaction_date: DF.Date | None
		transaction_id: DF.Link
	# end: auto-generated types

	pass
