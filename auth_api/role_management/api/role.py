from auth_api.role_management.services.role_service import create_role, get_all_roles
from auth_api.user_management.utils import response

import frappe

@frappe.whitelist(allow_guest=False, methods=["POST"])
def create():
    data = frappe.request.get_json()

    role_name   = data.get("role")
    description = data.get("description", "")

    try:
        result = create_role(role_name=role_name, description=description)

        return response.success(result, http_status_code=200)

    except ValueError as e:
        return response.error(str(e))

@frappe.whitelist(allow_guest=False, methods=["GET"])
def get():
    data = frappe.request.args

    try:
        page=int(data.get("page", 1))
        page_size=int(data.get("page_size", 10))

        search      = data.get("search", "").strip() or None

        result = get_all_roles(page, page_size, search)

        return response.send_response_list(
                            status = "success",
                            message = "Roles fetched successfully.",
                            data = result,
                            status_code = 200,
                            http_status = 200,
                        )

    except ValueError as e:
        return response.error(str(e))
