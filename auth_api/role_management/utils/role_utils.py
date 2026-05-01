import frappe

def validate_role_name(role_name: str) -> None:
    if not role_name:
        raise ValueError("'roleName' is required.")

    if frappe.db.exists("Role", role_name):
        raise ValueError(f"Role '{role_name}' already exists.")

def build_role_doc(role_name: str, description: str) -> dict:
    return {
        "doctype":     "Role",
        "role_name":   role_name,
        "description": description,
        "is_custom":   1,
        "desk_access": 0,
    }

def build_role_search_filter(search: str = None) -> list:
    if not search:
        return []

    return [
        ["Role", "role_name",   "like", f"%{search}%"],
    ]