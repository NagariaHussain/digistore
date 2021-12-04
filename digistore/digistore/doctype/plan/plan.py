# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document


class Plan(Document):
	def validate(self):
		set_of_assets = set(a.asset for a in self.assets)

		if len(set_of_assets) != len(self.assets):
			frappe.throw("Assets table contains duplicate entries")
