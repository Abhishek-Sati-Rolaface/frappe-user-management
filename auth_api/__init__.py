__version__ = "0.0.1"
import frappe.handler
from .overrides.whitelist import custom_is_whitelisted

frappe.handler.is_whitelisted = custom_is_whitelisted