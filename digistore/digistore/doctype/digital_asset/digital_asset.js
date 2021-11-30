// Copyright (c) 2021, Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on("Digital Asset", {
  refresh: function (frm) {
    if (!frm.doc.s3_file_url) {
      let btn = frm.add_custom_button(
        "Upload File to S3",
        () => {
          frappe.confirm(
            "This action will upload the attachments to this document to S3 bucket. Continue?",
            () => {
              frappe.show_alert({
                message: "Upload Started..",
                indicator: "green",
              });

              frm
                .call({
                  doc: frm.doc,
                  method: "upload_to_s3",
                  btn,
                })
                .then((r) => {
                  frm.refresh();
                  frappe.msgprint("Upload Complete.", (indicator = "green"));
                });
            }
          );
        },
        "Actions"
      );
    }
  },
  get_from_s3: function (frm) {
    const w = window.open(frappe.urllib.get_full_url(frm.doc.s3_file_url));
    if (!w) {
      frappe.msgprint("Please enable pop-ups");
    }
  },
});
