from frappe.permissions import add_permission, update_permission_property
import frappe

def create_permission(permissions, role_name):
    for permission in permissions:
        doctype = permission["module"]
        ptype_map = {k: v for k, v in permission.items() if k != "module"}

        def clear_cache():
            frappe.clear_cache(doctype = doctype)

        if not frappe.db.get_value("Custom DocPerm", dict(parent=doctype, role=role_name)):
            add_permission(doctype = doctype, role = role_name)

        for ptype, value in ptype_map.items():
            update_permission_property(doctype=doctype, role=role_name, permlevel=0, ptype= ptype, value= value)

        frappe.db.after_commit.add(clear_cache)
