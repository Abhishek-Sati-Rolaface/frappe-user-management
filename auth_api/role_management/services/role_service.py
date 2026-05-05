from auth_api.role_management.services.permission_service import create_permission
from auth_api.role_management.utils.role_utils import build_role_search_filter, delete_removed_permissions, validate_role_exists, validate_role_name, build_role_doc
import frappe

def create_role(role_name: str, permission: list = []) -> dict:
   
    validate_role_name(role_name)

    role_data = build_role_doc(role_name)

    role = frappe.get_doc(role_data)
    role.insert(ignore_permissions=True)
    create_permission(permission, role.name)

    return {"roleId": role.name}

def update_role(role_id: str, permissions: list = []) -> dict:
   
    create_permission(permissions, role_id)
    incoming_modules = [perm["module"] for perm in permissions if perm.get("module")]

    delete_removed_permissions(role_id, incoming_modules)
    return {"roleId": role_id}

def update_role_status(role_id: str, is_disabled: bool):
    frappe.db.set_value("Role", role_id, "disabled", int(is_disabled))
    frappe.db.commit()

    return {
        "roleId":   role_id,
        "disabled": is_disabled,
    }

def get_all_roles(page, page_size, search: str = None) -> dict:
  
    or_filters    = build_role_search_filter(search=search)
    limit_start   = (page - 1) * page_size

    total = frappe.db.count("Role")

    roles = frappe.db.get_all(
        doctype    = "Role",
        or_filters = or_filters or None,
        fields       = ["name", "role_name", "disabled"],
        order_by     = "creation desc",
        limit_start  = limit_start,
        limit_page_length = page_size,
    )

    normalized = [
        {
            "Id": role.name,
            "roleName": role.role_name,
            "disabled": role.disabled
        }
        for role in roles
    ]

    total_pages = max(1, -(-total // page_size))

    return {
        "data": normalized,
        "pagination": {
            "page":        page,
            "page_size":   page_size,
            "total":       total,
            "total_pages": total_pages,
            "has_next":    page < total_pages,
            "has_prev":    page > 1,
        },
    }

def get_role(role_name: str) -> dict:

    validate_role_exists(role_name)

    role = frappe.db.get_value(
                "Role",
                role_name,
                ["name", "role_name"],
                as_dict=True,
            )

    raw_perms = frappe.db.get_all(
        "Custom DocPerm",
        filters={"role": role_name},
        fields=[
            "parent", "read", "write", "create", "delete",
            "print", "report", "import", "export",
        ],
    )
    if not raw_perms:
        raw_perms = frappe.get_all("DocPerm", filters={"role": role_name},
                        fields=[
                            "parent", "read", "write", "create", "delete",
                            "print", "report", "import", "export",
                        ])


    permissions = [
        {
            "module": perm.parent,
            "read": perm.read,
            "write": perm.write,
            "create": perm.create,
            "delete": perm.delete,
            "report": perm.report,
            "import": perm.get("import"),
            "export": perm.export,
        }
        for perm in raw_perms
    ]

    return {
        "roleId":      role.name,
        "roleName":    role.role_name,
        "permissions": permissions,
    }