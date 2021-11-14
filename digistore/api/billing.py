import frappe
from digistore.utils.payments import get_stripe
import math


class InvalidStripeWebhookEvent(Exception):
	http_status_code = 400


@frappe.whitelist()
def create_checkout_session(data=None):
	plan = frappe.get_doc("Plan", data["plan"])

	from digistore.utils.payments import get_stripe

	stripe = get_stripe()

	session = stripe.checkout.Session.create(
		payment_method_types=["card"],
		line_items=[
			{
				"price_data": {
					"currency": "usd",
					"product_data": {"name": plan.title,},
					"unit_amount": math.floor(plan.price * 100),
				},
				"quantity": 1,
			},
		],
		mode="payment",
		success_url=(
			"http://f22c-2409-4043-2011-55d5-2f09-3090-6459-c1da.ngrok.io/store/success"
		),
		cancel_url="http://f22c-2409-4043-2011-55d5-2f09-3090-6459-c1da.ngrok.io/store",
	)

	frappe.get_doc(
		{
			"doctype": "Store Purchase",
			"plan": plan.name,
			"product": plan.product,
			"purchased_by": frappe.session.user,
			"payment_indent_id": session.payment_intent,
		}
	).insert(ignore_permissions=True)

	return session.url


@frappe.whitelist(allow_guest=True)
def handle_stripe_webhook():
	current_user = frappe.session.user
	form_dict = frappe.local.form_dict

	try:
		payload = frappe.request.get_data()
		signature = frappe.get_request_header("Stripe-Signature")
		# parse payload will verify the request
		event = parse_payload(payload, signature)
		# set user to Administrator, to not have to do ignore_permissions everywhere
		frappe.set_user("Administrator")

		print(
			{
				"doctype": "Stripe Webhook Log",
				"name": event.id,
				"payload": form_dict,
				"event_type": event.type,
			}
		)

		if event.type == "checkout.session.completed":
			sp_doc = frappe.get_doc(
				"Store Purchase", {"payment_indent_id": form_dict["payload"]["payment_intent"]}
			)
			sp_doc.paid = True
			sp_doc.save()
	except Exception:
		frappe.db.rollback()
		frappe.log_error(title="Stripe Webhook Handler")
		frappe.set_user(current_user)
		raise Exception


def parse_payload(payload, signature):
	secret = frappe.db.get_single_value("DigiStore Settings", "stripe_webhook_secret")
	stripe = get_stripe()
	try:
		return stripe.Webhook.construct_event(payload, signature, secret)
	except ValueError:
		# Invalid payload
		frappe.throw("Invalid Payload", InvalidStripeWebhookEvent)
	except stripe.error.SignatureVerificationError:
		# Invalid signature
		frappe.throw("Invalid Signature", InvalidStripeWebhookEvent)