from frappe.permissions import add_permission, update_permission_property
import frappe

# def create_permission(permissions, role_name):
#     for permission in permissions:
#         doctype = permission["module"]
#         ptype_map = {k: v for k, v in permission.items() if k != "module"}

#         def clear_cache():
#             frappe.clear_cache(doctype = doctype)

#         if not frappe.db.get_value("Custom DocPerm", dict(parent=doctype, role=role_name)):
#             add_permission(doctype = doctype, role = role_name)

#         for ptype, value in ptype_map.items():
            # update_permission_property(doctype=doctype, role=role_name, permlevel=0, ptype= ptype, value= value)

#         frappe.db.after_commit.add(clear_cache)


def create_permission(permissions: list, role_name: str) -> None:

    if not permissions:
        return

    existing_rows = frappe.db.get_all(
        "Custom DocPerm",
        filters = {"role": role_name},
        fields  = ["name", "parent"],
    )
    existing_map = {row.parent: row.name for row in existing_rows}

    to_insert = []
    to_update = []

    for permission in permissions:
        doctype  = permission["module"]
        ptype_map = {k: v for k, v in permission.items() if k != "module"}

        if doctype in existing_map:
            to_update.append({"doctype": doctype, "ptype_map": ptype_map})
        else:
            to_insert.append({"doctype": doctype, "ptype_map": ptype_map})

    for item in to_insert:
        doctype   = item["doctype"]
        ptype_map = item["ptype_map"]

        add_permission(doctype=doctype, role=role_name)

        frappe.db.set_value(
            "Custom DocPerm",
            {"parent": doctype, "role": role_name, "permlevel": 0},
            ptype_map,
        )

    for item in to_update:
        doctype   = item["doctype"]
        ptype_map = item["ptype_map"]
        ptype_map.pop("root_module", None)

        frappe.db.set_value(
            "Custom DocPerm",
            {"parent": doctype, "role": role_name, "permlevel": 0},
            ptype_map,
        )

    all_affected_doctypes = [p["module"] for p in permissions]

    def clear_cache_all(doctypes=all_affected_doctypes):
        for dt in doctypes:
            frappe.clear_cache(doctype=dt)

    frappe.db.after_commit.add(clear_cache_all)