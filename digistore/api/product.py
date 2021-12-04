import frappe

from typing import Dict, List
from digistore.api.billing import create_checkout_session


@frappe.whitelist()
def all_products() -> List:
	return frappe.db.get_all(
		"Digital Product",
		filters={"available": True},
		fields=["name", "image", "title", "description", "category", "short_description"],
	)


@frappe.whitelist()
def buy(plan: str) -> str:
	return create_checkout_session({"plan": plan})


@frappe.whitelist()
def get_data(product: str) -> Dict:
	try:
		# TODO: Refactor to use get_value
		sp = frappe.get_doc(
			"Store Purchase", {"purchased_by": frappe.session.user, "product": product}
		)
	except:
		frappe.throw("Make sure you have purchased the product.")

	asset_names = frappe.get_all("Plan Assets", filters={"parent": sp.plan}, pluck="asset")

	assets = frappe.get_all(
		"Digital Asset",
		filters={"name": ("in", asset_names)},
		fields=["s3_file_url", "file", "description", "type"],
	)

	return assets


@frappe.whitelist()
def get(name: str) -> Dict:
	product_data = {}

	product_doc = frappe.get_doc("Digital Product", name)
	product_plans = frappe.get_all(
		"Plan", filters={"product": name}, fields=["name", "price", "currency", "title"]
	)

	product_data["product_doc"] = product_doc
	product_data["product_plans"] = product_plans

	return product_data


@frappe.whitelist()
def purchased(user: str = None) -> List:
	user_products = []

	if not user:
		user = frappe.session.user

	user_purchases = frappe.get_all(
		"Store Purchase",
		filters={"purchased_by": user, "paid": True},
		fields=["product", "plan"],
	)

	for purchase in user_purchases:
		product = frappe.get_doc("Digital Product", purchase.product)
		plan = frappe.get_doc("Plan", purchase.plan)

		user_products.append({"product": product, "plan": plan})

	return user_products