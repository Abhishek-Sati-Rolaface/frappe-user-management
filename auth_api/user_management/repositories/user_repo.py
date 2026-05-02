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
            "roles": [{"role": role} for role in data.get("roleIds", [])],
            "gender": data["gender"],
            "birth_date": data["dob"],
            "phone": data["phone"],
            "mobile_no": data["mobile_no"]
        })

        user.insert(ignore_permissions=True)
        return user
    
    @staticmethod
    def get_users(search=None, limit_start=0, limit_page_length=10):

        or_filters = None

        if search:
            or_filters = [
                ["name", "like", f"%{search}%"],
                ["email", "like", f"%{search}%"],
                ["first_name", "like", f"%{search}%"],
                ["last_name", "like", f"%{search}%"],
                ["username", "like", f"%{search}%"],
            ]

        return frappe.get_all(
            "User",
            or_filters=or_filters,
            fields=[
                "name as id",
                "email",
                "full_name as name",
                "username",
                "enabled",
                "creation"
            ],
            limit_start=limit_start,
            limit_page_length=limit_page_length,
            order_by="creation desc"
        )