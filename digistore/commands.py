import click

import frappe
from frappe.commands import pass_context, get_site


@click.command("setup-ngrok-webhook")
@pass_context
def start_ngrok_and_set_webhook(context):
	from pyngrok import ngrok
	from digistore.utils.payments import get_stripe

	site = get_site(context)
	frappe.init(site=site)
	frappe.connect()

	port = frappe.conf.http_port or frappe.conf.webserver_port
	tunnel = ngrok.connect(port, host_header=site)
	public_url = tunnel.public_url
	print()
	print(f"{public_url} -> http://{site}:{port}")
	print(f"Inspect logs at {tunnel.api_url}")

	# Set temp ngrok tunnel url
	frappe.db.set_value("DigiStore Settings", None, "temp_ngrok_public_url", public_url)
	frappe.db.commit()

	stripe = get_stripe()
	url = f"{public_url}/api/method/digistore.api.billing.handle_stripe_webhook"
	stripe.WebhookEndpoint.modify(
		frappe.db.get_single_value("DigiStore Settings", "stripe_webhook_endpoint_id"),
		url=url,
	)
	print("Updated Stripe Webhook Endpoint")

	ngrok_process = ngrok.get_ngrok_process()
	try:
		# Block until CTRL-C or some other terminating event
		ngrok_process.proc.wait()
	except KeyboardInterrupt:
		print("Shutting down server...")
		frappe.destroy()
		ngrok.kill()


commands = [
	start_ngrok_and_set_webhook,
]
