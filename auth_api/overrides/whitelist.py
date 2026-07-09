import frappe
from frappe import _, bold
from frappe.exceptions import SessionExpired, PermissionError

def custom_is_whitelisted(method):
    from frappe.utils import sanitize_html

    is_guest = frappe.session.user == "Guest"

    if method not in frappe.whitelisted or (is_guest and method not in frappe.guest_methods):
        if is_guest:
            # Session expired / not logged in — clean message for the frontend
            summary = _("Session Expired. Please log in again.")
            detail = ""
            msg = f"<details><summary>{summary}</summary>{detail}</details>" if detail else summary
            frappe.throw(msg, SessionExpired, title=_("Session Expired") if is_guest else _("Method Not Allowed"))
        else:
            # Logged in, but hitting a non-whitelisted method — real bug, keep it verbose for devs
            summary = _("You are not permitted to access this resource.")
            detail = _("Function {0} is not whitelisted.").format(
                bold(f"{method.__module__}.{method.__name__}")
            )

        msg = f"<details><summary>{summary}</summary>{detail}</details>"
        frappe.throw(msg, PermissionError, title=_("Method Not Allowed"))


    if is_guest and method not in frappe.xss_safe_methods:
        for key, value in frappe.form_dict.items():
            if isinstance(value, str):
                frappe.form_dict[key] = sanitize_html(value)