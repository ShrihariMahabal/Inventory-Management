// Copyright (c) 2026, Shrihari Mahabal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry", {
    type(frm) {
        // Hide both first
        frm.toggle_display("from_warehouse", false);
        frm.toggle_display("to_warehouse", false);

        if (frm.doc.type === "Receipt") {
            frm.toggle_display("to_warehouse", true);
        }

        if (frm.doc.type === "Consume") {
            frm.toggle_display("from_warehouse", true);
        }

        if (frm.doc.type === "Transfer") {
            frm.toggle_display("from_warehouse", true);
            frm.toggle_display("to_warehouse", true);
        }
    },

    refresh(frm) {
        frm.trigger("type"); // ensure correct state on load
    }
});
