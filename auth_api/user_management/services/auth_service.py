import frappe
from frappe import auth
from auth_api.user_management.utils.common import generate_keys

def login_user(username, password):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=username, pwd=password)
        login_manager.post_login()
        
        # Clear what Frappe auto-added after post_login()
        frappe.response.pop("home_page", None)
        frappe.response.pop("full_name", None)
        frappe.response.pop("message", None)

    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        return{
            "status": "error",
            "message": "Authentication Error!"
        }
        

    # api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    return {
        "status": "success",
        "message":{
                    "message":"Authentication success",
                    "sid":frappe.session.sid,
                    # "api_key":user.api_key,
                    # "api_secret":api_generate,
                    "username":user.username,
                    "email":user.email,
                    "full_name":user.full_name,
                    "gender":user.gender,
                    "roles": frappe.get_roles()
                }
    }