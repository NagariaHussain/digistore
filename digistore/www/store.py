# Copyright (c) 2022, Hussain Nagaria and Contributors
# MIT License. See license.txt

import frappe

no_cache = 1


def get_context(context):
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()
	context.csrf_token = csrf_token