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

	def validate(self):
		self.calculate_total_amount()
		self.validate_member_exists()

	def before_submit(self):
		self.set_collected_by()
		self.validate_payment_details()

	def on_submit(self):
		self.update_transaction_fines()
		self.update_member_fines()

	def on_cancel(self):
		self.reverse_member_fines()
		self.reverse_transaction_fines()

	def calculate_total_amount(self):
		total = (
			(self.membership_fee or 0)
			+ (self.late_fee or 0)
			+ (self.damage_fee or 0)
			+ (self.other_fee or 0)
			+ (self.fine_amount or 0)
		)

		self.net_amount = total - (self.discount_amount or 0)
		self.total_amount = total

	def validate_member_exists(self):
		if not frappe.db.exists("Library Member", self.member):
			frappe.throw(_("Library Member {0} does not exist").format(self.member))

		member_status = frappe.db.get_value("Library Member", self.member, "membership_status")
		if member_status == "Cancelled":
			frappe.throw(_("Cannot collect fees for cancelled member {0}").format(self.member))

	def validate_payment_details(self):
		if self.payment_method in ["Card", "UPI", "Net Banking", "Cheque", "Demand Draft"]:
			if not self.reference_number:
				frappe.throw(_("Reference Number is required for {0} payment").format(self.payment_method))

		if self.net_amount <= 0:
			frappe.throw(_("Net amount must be greater than zero"))

	def set_collected_by(self):
		if not self.collected_by:
			self.collected_by = frappe.session.user

	def update_member_fines(self):
		if self.payment_type == "Fine Payment" and self.fine_amount > 0:
			member_doc = frappe.get_doc("Library Member", self.member)
			member_doc.update_total_fines()
			member_doc.save(ignore_permissions=True)

	def update_transaction_fines(self):
		if self.payment_type == "Fine Payment":
			for fine_detail in self.fine_details:
				if fine_detail.transaction_id:
					frappe.db.set_value("Book Transaction", fine_detail.transaction_id, "fine_paid", 1)

	def reverse_member_fines(self):
		if self.payment_type == "Fine Payment":
			member_doc = frappe.get_doc("Library Member", self.member)
			member_doc.update_total_fines()
			member_doc.save(ignore_permissions=True)

	def reverse_transaction_fines(self):
		if self.payment_type == "Fine Payment":
			for fine_detail in self.fine_details:
				if fine_detail.transaction_id:
					frappe.db.set_value("Book Transaction", fine_detail.transaction_id, "fine_paid", 0)

	@frappe.whitelist()
	def get_outstanding_fines(self):
		"""Get all outstanding fines for the member"""
		if not self.member:
			return []

		outstanding_fines = frappe.db.sql(
			"""
			SELECT
				name as transaction_id,
				book,
				fine_amount,
				transaction_date,
				due_date,
				return_date
			FROM `tabBook Transaction`
			WHERE member = %s
			AND docstatus = 1
			AND fine_amount > 0
			AND fine_paid = 0
			ORDER BY transaction_date DESC
		""",
			(self.member,),
			as_dict=1,
		)

		return outstanding_fines

	@frappe.whitelist()
	def load_outstanding_fines(self):
		outstanding_fines = self.get_outstanding_fines()

		# Clear existing fine details
		self.set("fine_details", [])

		total_fine_amount = 0

		for fine in outstanding_fines:
			self.append(
				"fine_details",
				{
					"transaction_id": fine.transaction_id,
					"book": fine.book,
					"fine_amount": fine.fine_amount,
					"transaction_date": fine.transaction_date,
					"due_date": fine.due_date,
					"return_date": fine.return_date,
				},
			)
			total_fine_amount += fine.fine_amount

		self.fine_amount = total_fine_amount
		self.calculate_total_amount()
