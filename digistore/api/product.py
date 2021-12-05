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
def get_data(purchase: str) -> Dict:
	purchase_data = {}

	store_purchase = frappe.db.get_value(
		"Store Purchase", purchase, ["purchased_by", "plan"], as_dict=True
	)

	if frappe.session.user != store_purchase.purchased_by:
		frappe.throw("Make sure you have purchased the product.")

	asset_names = frappe.get_all(
		"Plan Assets", filters={"parent": store_purchase.plan}, pluck="asset"
	)

	assets = frappe.get_all(
		"Digital Asset",
		filters={"name": ("in", asset_names)},
		fields=["s3_file_url", "file", "description", "type"],
	)

	purchase_data["assets"] = assets
	purchase_data["plan"] = frappe.db.get_value("Plan", store_purchase.plan, "title")

	return purchase_data


@frappe.whitelist()
def get(name: str) -> Dict:
	product_data = {}

	product_doc = frappe.get_doc("Digital Product", name)
	product_plans = frappe.get_all(
		"Plan", filters={"product": name}, fields=["name", "price", "currency", "title"]
	)

	product_data["product_doc"] = product_doc
	product_data["product_plans"] = product_plans

	has_user_purchased = product_doc.is_purchased_by_user(frappe.session.user)
	product_data["has_user_purchased"] = has_user_purchased

	return product_data


@frappe.whitelist()
def purchased(user: str = None) -> List:
	user_products = []

	if not user:
		user = frappe.session.user

	user_purchases = frappe.get_all(
		"Store Purchase",
		filters={"purchased_by": user, "paid": True},
		fields=["name", "product", "plan"],
	)

	for purchase in user_purchases:
		product = frappe.get_doc("Digital Product", purchase.product)
		plan = frappe.get_doc("Plan", purchase.plan)

		user_products.append(
			{"name": purchase.name, "product": product, "plan": plan,}
		)

	return user_products