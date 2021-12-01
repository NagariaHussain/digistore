import re
import boto3
import frappe
import random
import string
import datetime
import mimetypes


from os import PathLike
from typing_extensions import Self
from frappe.utils.password import get_decrypted_password


class S3Client:
	def __init__(self, bucket_name: str, region: str = None) -> Self:
		access_key_id = None
		secret_access_key = None

		try:
			access_key_id = frappe.db.get_single_value("DigiStore Settings", "access_key_id")
			secret_access_key = get_decrypted_password(
				"DigiStore Settings", "DigiStore Settings", "secret_access_key"
			)
		except:
			frappe.throw("Required credentials for AWS S3 not found in DigiStore Settings.")

		self.bucket_name = bucket_name
		self.region = region or "ap-south-1"  # 'Mumbai'

		self.client_object = boto3.client(
			"s3",
			aws_access_key_id=access_key_id,
			aws_secret_access_key=secret_access_key,
			region_name=self.region,
		)

	def upload_file_with_key(
		self, file_path: PathLike, file_name, parent_doctype, parent_name, is_private=True
	):
		content_type = mimetypes.guess_type(file_path)[0]
		key = self.generate_and_get_key(file_name, parent_doctype, parent_name)

		try:
			if is_private:
				self.client_object.upload_file(
					file_path,
					self.bucket_name,
					key,
					ExtraArgs={
						"ContentType": content_type,
						"Metadata": {"ContentType": content_type, "file_name": file_name},
					},
				)
			else:
				self.client_object.upload_file(
					file_path,
					self.bucket_name,
					key,
					ExtraArgs={
						"ContentType": content_type,
						"ACL": "public-read",
						"Metadata": {"ContentType": content_type,},
					},
				)
		except boto3.exceptions.S3UploadFailedError:
			frappe.throw("File Upload Failed. Please try again.")

		return key

	def generate_and_get_key(self, file_name, parent_doctype, parent_name) -> str:
		"""
		Generate keys for s3 objects uploaded with file name attached.
		"""
		hook_cmd = frappe.get_hooks().get("s3_key_generator")
		if hook_cmd:
			try:
				k = frappe.get_attr(hook_cmd[0])(
					file_name=file_name, parent_doctype=parent_doctype, parent_name=parent_name
				)
				if k:
					return k.rstrip("/").lstrip("/")
			except:
				pass

		file_name = file_name.replace(" ", "_")
		file_name = self.strip_special_chars(file_name)
		key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

		today = datetime.datetime.now()
		year = today.strftime("%Y")
		month = today.strftime("%m")
		day = today.strftime("%d")

		doc_path = None
		try:
			doc_path = frappe.db.get_value(
				parent_doctype, filters={"name": parent_name}, fieldname=["s3_folder_path"]
			)
			doc_path = doc_path.rstrip("/").lstrip("/")
		except Exception as e:
			print(e)

		if not doc_path:
			final_key = (
				year + "/" + month + "/" + day + "/" + parent_doctype + "/" + key + "_" + file_name
			)
			return final_key
		else:
			final_key = doc_path + "/" + key + "_" + file_name
			return final_key

	def strip_special_chars(self, file_name):
		"""
		Strips file charachters which doesnt match the regex.
		"""
		regex = re.compile("[^0-9a-zA-Z._-]")
		file_name = regex.sub("", file_name)
		return file_name

	def get_presigned_url(self, key, file_name=None):
		"""
		Get a presigned URL
		"""
		# Get URL Expiry time
		self.signed_url_expiry_time = (
			frappe.db.get_single_value("DigiStore Settings", "presigned_url_expiry") or 3600
		)

		params = {
			"Bucket": self.bucket_name,
			"Key": key,
		}
		if file_name:
			params["ResponseContentDisposition"] = "filename={}".format(file_name)

		url = self.client_object.generate_presigned_url(
			"get_object", Params=params, ExpiresIn=self.signed_url_expiry_time,
		)

		return url


# Inspired by (okay, okay, I copied a few methods from):
# Ref: https://github.com/zerodha/frappe-attachments-s3/blob/990bea903ed6477f5d681ea3171e2bc83164e240/frappe_s3_attachment/controller.py