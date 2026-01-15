# Copyright (c) 2026, Shrihari Mahabal and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestStockLedger(IntegrationTestCase):
	"""
	Integration tests for StockLedger.
	Use this class for testing interactions between multiple components.
	"""

	def test_stock_ledger_manual_insert(self):
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(doctype="Stock Ledger", item="TV", warehouse="LSR1 Shelf 1", qty_change=2).insert()

	def test_stock_ledger_immutability(self):
		ledger_entry_list = frappe.get_all("Stock Ledger", limit=1)
		if not ledger_entry_list:
			self.skipTest("No ledger entries to update/delete")
		
		sle = frappe.get_doc("Stock Ledger", ledger_entry_list[0].name)

		with self.assertRaises(frappe.ValidationError):
			sle.save()

		with self.assertRaises(frappe.ValidationError):
			sle.delete()