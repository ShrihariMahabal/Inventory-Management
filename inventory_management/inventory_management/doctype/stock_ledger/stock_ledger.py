# Copyright (c) 2026, Shrihari Mahabal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StockLedger(Document):
	def before_insert(self):
		frappe.throw("Cannot insert! Ledger is Immutable.")
	
	def on_update(self):
		frappe.throw("Cannot update! Ledger is Immutable.")
	
	def on_trash(self):
		frappe.throw("Cannot delete! Ledger is Immutable.")