from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in digistore/__init__.py
from digistore import __version__ as version

setup(
	name="digistore",
	version=version,
	description="OS",
	author="OS",
	author_email="hOSussain@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
