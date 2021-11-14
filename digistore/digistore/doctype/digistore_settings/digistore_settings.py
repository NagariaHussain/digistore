# Copyright (c) 2021, OS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from digistore.utils.payments import get_stripe


class DigiStoreSettings(Document):
	@frappe.whitelist()
	def create_stripe_webhook(self):
		stripe = get_stripe()
		url = frappe.utils.get_url("/api/method/digistore.api.billing.handle_stripe_webhook")
		webhook = stripe.WebhookEndpoint.create(
			url=url,
			enabled_events=[
				"payment_intent.requires_action",
				"payment_intent.payment_failed",
				"payment_intent.succeeded",
				"payment_method.attached",
				"invoice.payment_action_required",
				"invoice.payment_succeeded",
				"invoice.payment_failed",
				"invoice.finalized",
				"checkout.session.completed",
				"checkout.session.async_payment_failed",
				"checkout.session.async_payment_succeeded",
				"checkout.session.expired",
			],
		)
		self.stripe_webhook_endpoint_id = webhook["id"]
		self.stripe_webhook_secret = webhook["secret"]
		self.flags.ignore_mandatory = True
		self.save()
