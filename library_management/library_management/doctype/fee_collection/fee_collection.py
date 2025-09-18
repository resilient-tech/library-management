# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class FeeCollection(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from library_management.library_management.doctype.fee_collection_fine_detail.fee_collection_fine_detail import (
			FeeCollectionFineDetail,
		)

		amended_from: DF.Link | None
		collected_by: DF.Link | None
		damage_fee: DF.Currency
		discount_amount: DF.Currency
		fine_amount: DF.Currency
		fine_details: DF.Table[FeeCollectionFineDetail]
		late_fee: DF.Currency
		member: DF.Link
		membership_fee: DF.Currency
		naming_series: DF.Literal["PAY-.YYYY.-.#####"]
		net_amount: DF.Currency
		other_fee: DF.Currency
		payment_date: DF.Date
		payment_method: DF.Literal["Cash", "Card", "UPI", "Net Banking", "Cheque", "Demand Draft"]
		payment_status: DF.Literal["Paid", "Partial", "Refunded", "Cancelled"]
		payment_type: DF.Literal["Fine Payment", "Membership Fee", "Deposit", "Damage Fee", "Other"]
		reference_number: DF.Data | None
		remarks: DF.Text | None
		total_amount: DF.Currency
	# end: auto-generated types
	pass
