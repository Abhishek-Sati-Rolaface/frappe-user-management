from auth_api.user_management.api.schema import SignupSchema
from auth_api.user_management.utils import response
from auth_api.user_management.utils.pydantic_errors import format_pydantic_errors
import frappe
from auth_api.user_management.services import auth_service, user_service
from pydantic import ValidationError

@frappe.whitelist(allow_guest=True, methods=["POST"])
def login(usr, pwd):
    try:
        user_data = auth_service.login_user(usr, pwd)
        if user_data.get("status") == "error":
            return response.error(user_data.get("message"))
        return response.success(user_data.get("message"), http_status_code=200)
    except frappe.exceptions.AuthenticationError as e:
        return response.unauthorized(str(e))

@frappe.whitelist(allow_guest=True, methods=["POST"])
def signup(**payload):
    try:
        data = SignupSchema(**payload).model_dump()
        user = user_service.UserService.signup(data)
        if user.get("status") == "error":
            return response.error(user.get("message"))
        return response.success(user.get("message"), http_status_code=201)
    except ValidationError as e:
        return response.validation_error(format_pydantic_errors(e))

@frappe.whitelist(allow_guest=True, methods=["POST"])
def forgot_password(email: str):
    try:
        user = frappe.get_doc("User", email)

        user.reset_password(send_email=True)
        return response.success(
                                "Password reset link sent to your email, Please check your inbox", 
                                http_status_code=200
                            )
    except Exception as e:
        return response.error("Unable to process your request, Please try again later",
                                http_status_code=500
                            )
    
@frappe.whitelist(allow_guest=True, methods=["POST"])
def logout():
    # Please add SID in cookies to logout properly.
    try:
        frappe.local.login_manager.logout()
        return response.success("Logged out successfully")
    except Exception as e:
        return response.error("Unable to process your request, Please try again later",
                                http_status_code=500
                            )