from auth_api.user_management.utils import response
import frappe
from auth_api.user_management.services import auth_service

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    try:
        user_data = auth_service.login_user(usr, pwd)
        if user_data.get("status") == "error":
            return response.error(user_data.get("message"))
        return response.success(user_data.get("message"), http_status_code=200)
    except frappe.exceptions.AuthenticationError as e:
        return response.unauthorized(str(e))
