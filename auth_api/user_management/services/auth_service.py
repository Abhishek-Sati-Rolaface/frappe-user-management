import frappe
from frappe import auth
from auth_api.user_management.utils.common import generate_keys

def login_user(username, password):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=username.strip(), pwd=password.strip())
        login_manager.post_login()

    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        raise frappe.exceptions.AuthenticationError("Invalid username or password")

    # api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    roles = frappe.db.get_all(
                "Has Role",
                filters = {
                    "parent": user.name,
                    "parenttype": "User",
                }, pluck = "role",
            )    
    return {
        "status": "success",
        "message":{
                    "sid":frappe.session.sid,
                    # "api_key":user.api_key,
                    # "api_secret":api_generate,
                    "username":user.username,
                    "email":user.email,
                    "full_name":user.full_name,
                    "gender":user.gender,
                    "roles": roles
                }
    }