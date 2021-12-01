import frappe

from digistore.utils.s3_client import S3Client


@frappe.whitelist()
def upload_digital_asset_to_s3(doc, method=None):
	bucket_name = frappe.db.get_single_value("DigiStore Settings", "bucket_name")

	if not bucket_name:
		frappe.throw("S3 Bucket name not set in DigiStore Settings")

	attached_asset_file = frappe.get_all(
		"File",
		filters={
			"attached_to_doctype": "Digital Asset",
			"attached_to_field": "file",
			"attached_to_name": doc.name,
		},
		pluck="name",
		limit=1,
		order_by="creation desc",  # To get the latest attached one
	)

	if not attached_asset_file:
		frappe.throw("No file attached to this asset!")
	attached_asset_file = attached_asset_file[0]

	client = S3Client(bucket_name)

	# Protect thy asset!
	file = frappe.get_doc("File", attached_asset_file, for_update=True)
	file.is_private = True
	file.save()
	file.reload()

	path = file.file_url
	site_path = frappe.utils.get_site_path()
	parent_doctype = "Digital Asset"
	parent_name = doc.name
	file_path = site_path + path

	key = client.upload_file_with_key(
		file_path, file.file_name, parent_doctype, parent_name
	)

	method = "digistore.utils.asset_storage.generate_and_get_file"
	file_url = """/api/method/{0}?key={1}&file_name={2}""".format(
		method, key, file.file_name
	)

	doc.db_set("s3_file_url", file_url)
	frappe.db.commit()


@frappe.whitelist()
def generate_and_get_file(key=None, file_name=None):
	"""
	Function to stream file from s3.
	"""
	if key:
		bucket_name = frappe.db.get_single_value("DigiStore Settings", "bucket_name")

		if not bucket_name:
			frappe.throw("S3 Bucket name not set in DigiStore Settings")

		s3_client = S3Client(bucket_name)
		signed_url = s3_client.get_presigned_url(key, file_name)
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = signed_url
	else:
		frappe.local.response["body"] = "Key not found."


@frappe.whitelist()
def upload_digital_asset_to_s3_hook(doc, method):
	"""Hook version, so the below condition can be checked"""
	if not frappe.db.get_single_value(
		"DigiStore Settings", "upload_all_digital_assets_to_s3"
	):
		return

	# Why? Because the file was not getting attached before this hook is called.
	frappe.core.doctype.file.file.attach_files_to_document(doc, method)

	upload_digital_asset_to_s3(doc, method)