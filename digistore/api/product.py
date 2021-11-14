import frappe

from typing import List


@frappe.whitelist()
def purchased(user: str) -> List:
	user_products = []

	user_purchases = frappe.get_all(
		"Store Purchase", filters={"purchased_by": user}, fields=["product", "plan"]
	)

	for purchase in user_purchases:
		product = frappe.get_doc("Product", purchase.product)
		plan = frappe.get_doc("Plan", purchase.plan)

		user_products.append({"product": product, "plan": plan})

	return user_products