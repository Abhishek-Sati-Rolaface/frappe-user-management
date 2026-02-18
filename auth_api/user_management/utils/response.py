import frappe

def _clean():
    """Remove all Frappe auto-populated keys"""
    for key in ["home_page", "full_name", "message", "_server_messages"]:
        frappe.response.pop(key, None)
    frappe.clear_messages()

def success(data=None, http_status_code=200):
    _clean()
    frappe.local.response.http_status_code = http_status_code
    frappe.response["message"] = {
        "status"  : "success",
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