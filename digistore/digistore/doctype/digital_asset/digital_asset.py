# Copyright (c) 2021, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from digistore.utils.asset_storage import upload_digital_asset_to_s3


class DigitalAsset(Document):
	@frappe.whitelist()
	def upload_to_s3(self):
		return upload_digital_asset_to_s3(self)
