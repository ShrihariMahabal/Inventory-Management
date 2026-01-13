// Copyright (c) 2026, Shrihari Mahabal and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Ledger Report"] = {
	filters: [
		{
		"fieldname": "item",
		"fieldtype": "Link",
		"label": "Item",
		"mandatory": 0,
		"options": "Item",
		"wildcard_filter": 0
		},
		{
		"fieldname": "warehouse",
		"fieldtype": "Link",
		"label": "Warehouse",
		"mandatory": 0,
		"options": "Warehouse",
		"wildcard_filter": 0
		},
		{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "From Date",
		"mandatory": 0,
		"wildcard_filter": 0
		},
		{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": "To Date",
		"mandatory": 0,
		"wildcard_filter": 0
		}
	],
};
