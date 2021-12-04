# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DigitalProduct(Document):
	def is_purchased_by_user(self, user):
		return frappe.db.exists(
			"Store Purchase", {"purchased_by": user, "product": self.name, "paid": True},
		)
