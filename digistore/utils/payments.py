import frappe
import stripe


def get_stripe():
	from frappe.utils.password import get_decrypted_password

	if not hasattr(frappe.local, "digistore_stripe_object"):
		stripe_account = frappe.db.get_single_value("DigiStore Settings", "stripe_account")
		secret_key = get_decrypted_password(
			"Stripe Settings", stripe_account, "secret_key", raise_exception=False
		)

		if not (stripe_account and secret_key):
			frappe.throw(
				"Setup stripe via DigiStore Settings before using"
				" digistore.utils.payments.get_stripe"
			)

		stripe.api_key = secret_key
		frappe.local.digistore_stripe_object = stripe

	return frappe.local.digistore_stripe_object
