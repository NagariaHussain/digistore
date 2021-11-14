import frappe
import stripe


def get_stripe():
	from frappe.utils.password import get_decrypted_password

	if not hasattr(frappe.local, "digistore_stripe_object"):
		secret_key = get_decrypted_password(
			"DigiStore Settings", "DigiStore Settings", "secret_key", raise_exception=False
		)

		if not secret_key:
			frappe.throw(
				"Setup stripe via DigiStore Settings before using digistore.api.payments.get_stripe"
			)

		stripe.api_key = secret_key
		frappe.local.digistore_stripe_object = stripe

	return frappe.local.digistore_stripe_object