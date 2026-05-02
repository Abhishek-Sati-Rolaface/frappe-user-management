import frappe
class UserRepository:
    @staticmethod
    def create_user(data: dict) -> frappe.model.document.Document:
        print(data)
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