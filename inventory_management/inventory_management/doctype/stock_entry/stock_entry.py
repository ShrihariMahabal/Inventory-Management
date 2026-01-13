# Copyright (c) 2026, Shrihari Mahabal and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


class StockEntry(Document):
	def validate(self):
		# check whether there are enough items to move out of source warehouse in case of Transfer / Consume
		Ledger = DocType("Stock Ledger")
		exiting_warehouse = self.from_warehouse

		if self.type == "Transfer" and self.from_warehouse == self.to_warehouse:
			frappe.throw("From and To Warehouse cannot be same")
		if len(self.entry_items) == 0:
			frappe.throw("Stock Entry Items can't be empty")
		if self.type == "Consume" or self.type == "Transfer":
			for entry_item in self.entry_items:
				item_name = entry_item.item_name
				if entry_item.quantity <= 0:
					frappe.throw("Quantity can't be negative")

				result = (frappe.qb.from_(Ledger).select(Sum(Ledger.qty_change)).where((Ledger.warehouse == exiting_warehouse) & (Ledger.item == item_name) & (Ledger.date <= self.date)).run())
				balance = result[0][0]
				if balance is None or balance < entry_item.quantity:
					frappe.throw(f"Not Enough Items to move out of warehouse: {self.from_warehouse}", title="Insufficient Stock")

	def on_submit(self):
		entering_warehouse = self.to_warehouse
		exiting_warehouse = self.from_warehouse if self.type != "Receipt" else ""

		for entry_item in self.entry_items:
			item_name = entry_item.item_name
			qty_change = entry_item.quantity
			rate = entry_item.rate

			if self.type == "Receipt":
				self.create_ledger_entry(entering_warehouse, item_name, qty_change, rate)
			elif self.type == "Consume":
				avg_value = self.get_current_avg_value(item_name, exiting_warehouse)
				self.create_ledger_entry(exiting_warehouse, item_name, -qty_change, avg_value)
			else:
				avg_value = self.get_current_avg_value(item_name, exiting_warehouse)
				self.create_ledger_entry(exiting_warehouse, item_name, -qty_change, avg_value)
				self.create_ledger_entry(entering_warehouse, item_name, qty_change, avg_value)


	def create_ledger_entry(self, warehouse, item_name, qty_change, rate):
		ledger_entry = frappe.get_doc(doctype="Stock Ledger", item=item_name, warehouse=warehouse, qty_change=qty_change, rate=rate, date=self.date, voucher_no=self.name)
		ledger_entry.insert()

	def get_current_avg_value(self, item_name, warehouse):
		Ledger = DocType("Stock Ledger")
		result = (frappe.qb.from_(Ledger).select(Sum(Ledger.qty_change * Ledger.rate) / Sum(Ledger.qty_change)).where((Ledger.item == item_name) & (Ledger.warehouse == warehouse)).run())
		avg_value = result[0][0]
		frappe.msgprint(f"Value: {avg_value}")
		return avg_value

	def on_cancel(self):
		stock_ledger_items = frappe.db.get_all("Stock Ledger", filters={"voucher_no": self.name}, fields=["*"])
		for row in stock_ledger_items:
			self.create_ledger_entry(row.warehouse, row.item, -row.qty_change, row.rate)