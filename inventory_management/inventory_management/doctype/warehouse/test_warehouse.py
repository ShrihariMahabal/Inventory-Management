# Copyright (c) 2026, Shrihari Mahabal and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from inventory_management.tests.utils import make_warehouse


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestWarehouse(IntegrationTestCase):
    """
    Integration tests for Warehouse.
    Use this class for testing interactions between multiple components.
    """

    def setUp(self):
        super().setUp()

        self.parent = make_warehouse("Lucknow", is_group=1, parent_warehouse=None)
        self.child = make_warehouse(
            "Lucknow Shelf 1", is_group=0, parent_warehouse=self.parent
        )

    def test_parent_child_relation(self):
        self.assertEqual(
            frappe.db.get_value("Warehouse", self.child, "parent_warehouse"),
            self.parent,
        )
