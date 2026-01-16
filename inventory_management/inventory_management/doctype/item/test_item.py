# Copyright (c) 2026, Shrihari Mahabal and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from inventory_management.tests.utils import make_item

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestItem(IntegrationTestCase):
	"""
	Integration tests for Item.
	Use this class for testing interactions between multiple components.
	"""
	def setUp(self):
		super().setUp()

		self.item_name = "Test TV"
		self.uom = "nos"
		self.item_id = make_item(self.item_name, self.uom)
	
	def test_item_created(self):
		self.assertTrue(frappe.db.exists("Item", self.item_id))