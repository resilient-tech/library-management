# Copyright (c) 2025, Library Management and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Author(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		author_name: DF.Data
		biography: DF.Text | None
		birth_date: DF.Date | None
		death_date: DF.Date | None
		nationality: DF.Data | None
	# end: auto-generated types

	pass
