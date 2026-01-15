# Copyright (c) 2026, Shrihari Mahabal and Contributors
# See license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum
from frappe.tests import IntegrationTestCase
from inventory_management.tests.utils import make_item, make_warehouse, make_receipt, make_consume, make_transfer


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestStockEntry(IntegrationTestCase):
	"""
	Integration tests for StockEntry.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		super().setUp()

		self.Ledger = DocType("Stock Ledger")
		self.item_id = make_item("Test Laptop", "nos")
		# item = frappe.get_doc("Stock Ledger", self.item_id)
		# self.items = [item]
		self.date = "14-01-2026"
		self.wh2 = make_warehouse("Lucknow Store 1")
		self.wh1 = make_warehouse("Lucknow Store 2")

	
	def test_receipt(self):
		items = [{"item_name": self.item_id, "quantity": 10, "rate": 10000}]
		doc = make_receipt(self.date, self.wh1, items)
		doc.submit()
		self.assertEqual(self.get_qty(self.wh1), 10)
		self.assertEqual(self.get_value(self.wh1), 100000.0)

	def test_consume(self):
		items = [{"item_name": self.item_id, "quantity": 2}]
		doc = make_consume(self.date, self.wh1, items)
		doc.submit()
		self.assertEqual(self.get_qty(self.wh1, 8))

	# def test_consume_fails_when_insufficient_stock(self):
	# 	with self.assertRaises(frappe.ValidationError):
	# 		items = [{"item_name": self.item_id, "quantity": 20}]
	# 		doc = make_consume(self.date, self.wh1, items)
	# 		doc.submit()
	
	# def test_transfer_preserves_qty(self):
	# 	items = [{"item_name": self.item_id, "quantity": 2}]
	# 	doc = make_transfer(self.date, self.wh1, self.wh2, items)
	# 	doc.submit()
	# 	self.assertEqual(self.get_qty(self.wh1), 6)
	# 	self.assertEqual(self.get_qty(self.wh2), 2)
	
	# def test_moving_average(self):
	# 	items = [{"item_name": self.item_id, "quantity": 10, "rate": 22000}]
	# 	receipt1 = make_receipt(self.date, self.wh2, items)
	# 	result = (frappe.qb.from_(self.Ledger).select(Sum(self.Ledger.qty_change * self.Ledger.rate) / Sum(self.Ledger.qty_change)).where((self.Ledger.item == self.item_id) & (self.Ledger.warehouse == self.wh2)).run())
	# 	avg_rate = result[0][0]
	# 	self.assertEqual(avg_rate, 20000.0)


	def get_qty(self, warehouse):
		result = (frappe.qb.from_(self.Ledger).select(Sum(self.Ledger.qty_change)).where((self.Ledger.item == self.item_id) & (self.Ledger.warehouse == warehouse)).run())
		return result[0][0] or 0

	def get_value(self, warehouse):
		result = (frappe.qb.from_(self.Ledger).select(Sum(self.Ledger.qty_change * self.Ledger.rate)).where((self.Ledger.item == self.item_id) & (self.Ledger.warehouse == warehouse)).run())
		return result[0][0] or 0