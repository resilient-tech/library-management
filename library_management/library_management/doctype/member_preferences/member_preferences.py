# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MemberPreferences(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		preference_type: DF.Literal["Genre", "Author", "Language", "Format"]
		preference_value: DF.Data
		priority: DF.Literal["High", "Medium", "Low"]
	# end: auto-generated types

	pass
