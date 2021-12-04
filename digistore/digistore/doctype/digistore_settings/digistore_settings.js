// Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on("DigiStore Settings", {
  create_stripe_webhook(frm) {
    frm.call("create_stripe_webhook");
  },
  // refresh: function(frm) {

  // }
});
