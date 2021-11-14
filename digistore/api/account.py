import frappe


@frappe.whitelist()
def get():
	user = frappe.session.user
	if not frappe.db.exists("User", user):
		frappe.throw("Account does not exist")

	return {"user": frappe.get_doc("User", user)}
