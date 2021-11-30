import frappe

from digistore.utils.s3_client import S3Client


@frappe.whitelist()
def upload_digital_asset_to_s3(doc, method=None):
	bucket_name = frappe.db.get_single_value("DigiStore Settings", "bucket_name")

	if not bucket_name:
		frappe.throw("S3 Bucket name not set in DigiStore Settings")

	attached_asset_file = frappe.get_all(
		"File",
		fields=["name", "file_url"],
		filters={
			"attached_to_doctype": "Digital Asset",
			"attached_to_field": "file",
			"attached_to_name": doc.name,
		},
		limit=1,
		pluck="name",
	)

	if not attached_asset_file:
		frappe.throw("No file attached to this asset!")

	client = S3Client(bucket_name)

	# TODO: Can be optimized, by not using get_doc
	file_doc = frappe.get_doc("File", attached_asset_file[0])
	path = file_doc.file_url
	site_path = frappe.utils.get_site_path()
	parent_doctype = file_doc.attached_to_doctype
	parent_name = file_doc.attached_to_name

	if not file_doc.is_private:
		file_path = site_path + "/public" + path
	else:
		file_path = site_path + path

	key = client.upload_file_with_key(
		file_path, file_doc.file_name, parent_doctype, parent_name, file_doc.is_private
	)

	if file_doc.is_private:
		method = "digistore.utils.asset_storage.generate_and_get_file"
		file_url = """/api/method/{0}?key={1}&file_name={2}""".format(
			method, key, file_doc.file_name
		)
	else:
		file_url = "{}/{}/{}".format(
			client.client_object.meta.endpoint_url, client.bucket_name, key
		)

	doc.s3_file_url = file_url  # Set Digital Asset doc's s3 file field
	doc.save()

	frappe.db.commit()
	doc.reload()


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
