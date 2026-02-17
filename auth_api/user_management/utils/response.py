# response.py

import frappe

def success(data=None):
    frappe.response.clear()
    frappe.response["message"] = {
        "status": "success",
        "data": data
    }

def error(message=None, http_status_code=400):
    frappe.response.clear()
    frappe.local.response.http_status_code = http_status_code
    
    frappe.response["message"] = {
        "status": "error",
        "message": message
    }