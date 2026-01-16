# Copyright (c) 2026, Shrihari Mahabal and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


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
            "fieldname": "item",
            "fieldtype": "Link",
            "label": "Item",
            "options": "Item",
            "width": 0,
        },
        {
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "label": "Warehouse",
            "options": "Warehouse",
            "width": 0,
        },
        {
            "fieldname": "quantity",
            "fieldtype": "Float",
            "label": "Quantity",
            "width": 0,
        },
        {
            "fieldname": "stock_value",
            "fieldtype": "Currency",
            "label": "Stock Value",
            "width": 0,
        },
        {
            "fieldname": "avg_rate",
            "fieldtype": "Currency",
            "label": "Average Rate",
            "width": 0,
        },
    ]


def get_data(filters: dict | None = None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    Ledger = DocType("Stock Ledger")
    query = (
        frappe.qb.from_(Ledger)
        .select(
            Ledger.item,
            Ledger.warehouse,
            Sum(Ledger.qty_change).as_("quantity"),
            Sum(Ledger.qty_change * Ledger.rate).as_("stock_value"),
        )
        .groupby(Ledger.item, Ledger.warehouse)
    )

    if filters.get("item"):
        query = query.where(Ledger.item == filters["item"])

    if filters.get("warehouse"):
        query = query.where(Ledger.warehouse == filters["warehouse"])

    if filters.get("as_on_date"):
        query = query.where(Ledger.date <= filters["as_on_date"])

    result = query.run(as_dict=True)

    for row in result:
        if row["quantity"] > 0:
            row["avg_rate"] = row["stock_value"] / row["quantity"]
        else:
            row["avg_rate"] = None

    return result
