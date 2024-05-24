# Copyright (c) 2024, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Provision(Document):

	@frappe.whitelist()
	def add_details(self):
		pass

	#def before_save(self):
	#	self.add_details()
				


