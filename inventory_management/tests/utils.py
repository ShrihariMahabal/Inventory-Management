import frappe

def make_item(item_name="Test TV", uom="nos"):
    item_doc = frappe.get_doc(doctype="Item", item_name=item_name, uom=uom).insert()
    return item_doc.name

def make_warehouse(warehouse_name, is_group=0, parent_warehouse=None):
    if not frappe.db.exists("Warehouse", warehouse_name):
        warehouse_entry = frappe.get_doc(doctype="Warehouse", warehouse_name=warehouse_name, is_group=is_group, parent_warehouse=parent_warehouse)
        warehouse_entry.insert()
    return warehouse_name

def make_receipt(date, to_warehouse, entry_items):
    receipt_entry = frappe.get_doc(doctype="Stock Entry", type="Receipt", date=date, to_warehouse=to_warehouse, entry_items=entry_items)
    receipt_entry.insert()
    return receipt_entry

def make_consume(date, from_warehouse, entry_items):
    consume_entry = frappe.get_doc(doctype="Stock Entry", type="Consume", date=date, from_warehouse=from_warehouse, entry_items=entry_items).insert()
    return consume_entry

def make_transfer(date, from_warehouse, to_warehouse, entry_items):
    transfer_entry = frappe.get_doc(doctype="Stock Entry", type="Transfer", date=date, from_warehouse=from_warehouse, to_warehouse=to_warehouse, entry_items=entry_items).insert()
    return transfer_entry