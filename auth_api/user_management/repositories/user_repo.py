from auth_api.user_management.utils.project_enum import ROLE_MAP
import frappe

class UserRepository:
    @staticmethod
    def create_user(data: dict) -> frappe.model.document.Document:
        user = frappe.get_doc({
            "doctype": "User",
            "email": data["email"],
            "first_name": data["firstName"],
            "middle_name": data.get("middleName"),
            "last_name": data["lastName"],
            "username": data["username"],
            "language": data.get("language"),
            "time_zone": data.get("timezone"),
            "enabled": 1,
            "roles": []
        })

        for role_id in data.get("roleIds", []):
            role_name = ROLE_MAP.get(role_id)
            if role_name:
                user.append("roles", {"role": role_name})

        user.insert(ignore_permissions=True)
        return user