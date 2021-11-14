import frappe
from digistore.utils.payments import get_stripe


class InvalidStripeWebhookEvent(Exception):
	http_status_code = 400


@frappe.whitelist(allow_guest=True)
def handle_stripe_webhook():
	pass


def parse_payload(payload, signature):
	secret = frappe.db.get_single_value("Press Settings", "stripe_webhook_secret")
	stripe = get_stripe()
	try:
		return stripe.Webhook.construct_event(payload, signature, secret)
	except ValueError:
		# Invalid payload
		frappe.throw("Invalid Payload", InvalidStripeWebhookEvent)
	except stripe.error.SignatureVerificationError:
		# Invalid signature
		frappe.throw("Invalid Signature", InvalidStripeWebhookEvent)