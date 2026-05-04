import frappe

def validate_role_name(role_name: str) -> None:
    if not role_name:
        raise ValueError("'roleName' is required.")

    if frappe.db.exists("Role", role_name):
        raise ValueError(f"Role '{role_name}' already exists.")

def build_role_doc(role_name: str) -> dict:
    return {
        "doctype":     "Role",
        "role_name":   role_name,
        "is_custom":   1,
        "desk_access": 0,
    }

def build_role_search_filter(search: str = None) -> list:
    if not search:
        return []

    return [
        ["Role", "role_name",   "like", f"%{search}%"],
    ]

def validate_role_exists(role_name: str) -> None:
    """Raise ValueError if role does not exist."""
    if not frappe.db.exists("Role", role_name):
        raise ValueError(f"Role '{role_name}' not found.")
    
def delete_removed_permissions(role_name: str, incoming_modules: list[str]) -> None:

    existing_modules = frappe.db.get_all(
                            "Custom DocPerm",
                            filters = {"role": role_name},
                            pluck   = "parent",
                        )

    modules_to_delete = [m for m in existing_modules if m not in incoming_modules]

    if not modules_to_delete:
        return

    for module in modules_to_delete:
        custom_docperms = frappe.db.get_values(
                                "Custom DocPerm", {"parent": module, "role": role_name}
                            )
        for name in custom_docperms:
            frappe.delete_doc("Custom DocPerm", name, ignore_permissions=True, force=True)