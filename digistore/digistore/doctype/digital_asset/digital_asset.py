# Copyright (c) 2021, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from digistore.utils.asset_storage import upload_digital_asset_to_s3


class DigitalAsset(Document):
	@frappe.whitelist()
	def upload_to_s3(self):
		return upload_digital_asset_to_s3(self)

	def is_purchased_by_user(self, user):
		user_purchased_plans = frappe.get_all(
			"Store Purchase", filters={"purchased_by": user, "paid": True,}, pluck="plan"
		)

		user_purchased_assets = frappe.get_all(
			"Plan Assets", filters={"parent": ("in", user_purchased_plans)}, pluck="asset"
		)

		return self.name in user_purchased_assets
