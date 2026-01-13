# Copyright (c) 2026, Shrihari Mahabal and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum, Abs


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
		"fieldname": "posting_date",
		"fieldtype": "Date",
		"label": "Date",
		"width": 0
		},
		{
		"fieldname": "item",
		"fieldtype": "Link",
		"label": "Item",
		"options": "Item",
		"width": 0
		},
		{
		"fieldname": "warehouse",
		"fieldtype": "Link",
		"label": "Warehouse",
		"options": "Warehouse",
		"width": 0
		},
		{
		"fieldname": "qty_change",
		"fieldtype": "Float",
		"label": "Quantity Change",
		"width": 0
		},
		{
		"fieldname": "rate",
		"fieldtype": "Currency",
		"label": "Rate",
		"width": 0
		},
		{
		"fieldname": "value",
		"fieldtype": "Currency",
		"label": "Value",
		"width": 0
		},
		{
		"fieldname": "voucher_no",
		"fieldtype": "Link",
		"label": "Voucher No",
		"options": "Stock Entry",
		"width": 0
		}
	]


def get_data(filters: dict | None = None) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	Ledger = DocType("Stock Ledger")

	query = (frappe.qb.from_(Ledger).select(
		(Ledger.date).as_("posting_date"),
		Ledger.item,
		Ledger.warehouse,
		Ledger.qty_change,
		Ledger.rate,
		Abs(Ledger.qty_change * Ledger.rate).as_("value"),
		Ledger.voucher_no
	))

	if filters.get("item"):
		query = query.where(Ledger.item == filters["item"])
	
	if filters.get("warehouse"):
		query = query.where(Ledger.warehouse == filters["warehouse"])
	
	if filters.get("from_date"):
		query = query.where(Ledger.date >= filters["from_date"])
	
	if filters.get("to_date"):
		query = query.where(Ledger.date <= filters["to_date"])
	
	result = query.run(as_dict=True)
	return result