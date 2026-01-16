# Copyright (c) 2026, Shrihari Mahabal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StockLedger(Document):
    def before_insert(self):
        if not frappe.flags.allow_stock_ledger_insert:
            frappe.throw(
                "Stock Ledger is system-generated and cannot be created manually."
            )

    def on_update(self):
        if self.flags.in_insert:
            return
        frappe.throw("Cannot update! Ledger is Immutable.")

    def on_trash(self):
        frappe.throw("Cannot delete! Ledger is Immutable.")
