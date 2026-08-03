import frappe
import json
from frappe import _

#@TODO: This function is may breaks the existing OAuth2 flow, need to check if it is safe to use this function in production.

def validate_bearer_sid():
    cookies = frappe.get_request_header("Cookie", "")
    if not cookies or "sid=Guest" in cookies:
        auth_header = frappe.get_request_header("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return

        sid = auth_header[len("Bearer "):].strip()
        if not sid:
            return

        sessions = frappe.qb.DocType("Sessions")
        sessions_data = (
                    frappe.qb.from_(sessions)
                    .select(sessions.user, sessions.sessiondata, sessions.sid)
                    .where(sessions.sid == sid)
                ).run(as_dict=True)
        if not sessions_data:
            frappe.throw(_("Invalid or expired session token"), frappe.AuthenticationError)

        user = sessions_data[0].user

        frappe.set_user(user)
        session_data = frappe.safe_decode(sessions_data[0].sessiondata)
        session_data = json.loads(session_data)
        full_name = frappe.db.get_value("User", user, "full_name")

        frappe.local.cookie_manager.init_cookies()
        frappe.local.cookie_manager.set_cookie("full_name", full_name, deduplicate=True)
        frappe.local.cookie_manager.set_cookie("user_id", session_data.get("user"), deduplicate=True)
        frappe.local.cookie_manager.set_cookie("user_lang", frappe.local.lang, deduplicate=True)
        frappe.local.cookie_manager.set_cookie("sid", sid, deduplicate=True)
        frappe.loacal.cookie_manager.set_cookie("SameSite", None, deduplicate=True)


