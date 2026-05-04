import frappe
from frappe.exceptions import PermissionError

def _clean():
    """Remove all Frappe auto-populated keys"""
    for key in ["home_page", "full_name", "message", "_server_messages"]:
        frappe.response.pop(key, None)
    frappe.clear_messages()

def success(data=None, message=None ,http_status_code=200):
    _clean()
    frappe.local.response.http_status_code = http_status_code
    frappe.response["message"] = {
        "status"  : "success",
        "message": message,
        "data"    : data
    }

def error(message="Something went wrong", errors=None, http_status_code=400):
    _clean()
    frappe.local.response.http_status_code = http_status_code
    frappe.response["message"] = {
        "status"  : "error",
        "message" : message,
        **({"errors": errors} if errors else {})
    }

def unauthorized(message="Unauthorized"):
    error(message=message, http_status_code=401)


def not_found(message="Resource not found"):
    error(message=message, http_status_code=404)


def validation_error(errors: dict):
    error(
        message = "Validation failed",
        errors  = errors,
        http_status_code = 422
    )

def handle_exception(e):
    if isinstance(e, PermissionError):
        frappe.clear_messages()
        frappe.local.response.http_status_code = 403
        frappe.response.clear()
        frappe.response["message"] = {
            "status": "error",
            "message": "Forbidden"
        }
        return True

    return False

def send_response_list(status="success", message="", data=None, status_code=200, http_status=200):

    response_payload = {
        "status_code": status_code,
        "status": status,
        "message": message
    }

    if data is not None:
        if isinstance(data, dict) and "data" in data:
            response_payload["data"] = data.get("data", [])
            if "pagination" in data:
                response_payload["pagination"] = data.get("pagination", {})
        elif isinstance(data, list):
            response_payload["data"] = data
        else:
            response_payload["data"] = data

    frappe.local.response = frappe._dict(response_payload)
    frappe.local.response.http_status_code = http_status