from auth_api.role_management.utils.role_utils import build_role_search_filter, validate_role_name, build_role_doc
import frappe

def create_role(role_name: str, description: str = "") -> dict:
   
    validate_role_name(role_name)

    role_data = build_role_doc(role_name, description)

    role = frappe.get_doc(role_data)
    role.insert(ignore_permissions=True)
    # frappe.db.commit()

    return {"roleId": role.name}

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
            "roleNa": role.role_name,
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