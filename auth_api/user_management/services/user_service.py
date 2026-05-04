from auth_api.user_management.repositories.user_repo import UserRepository
import frappe
class UserService:

    @staticmethod
    def signup(payload: dict) -> dict:
        try:
            frappe.db.begin()

            UserRepository.create_user(payload)

            return {
                "status": "success",
                "message": "User created successfully, Please check your email for login credentials"
            }

        except Exception:
            frappe.db.rollback()
            raise

    @staticmethod
    def get_users(page=1, page_size=10, search=""):

        limit_start = (page - 1) * page_size

        users = UserRepository.get_users(
            search=search,
            limit_start=limit_start,
            limit_page_length=page_size
        )

        total = len(users)

        total_pages = (total + page_size - 1) // page_size
        print(type(users))
        return {
            "status": "success",
            "data": users,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            }
        }

    @staticmethod
    def update_user_details(payload:dict) -> dict:
        try:
            frappe.db.begin()
    
            UserRepository.update_user(payload["userId"],payload)

            return {
                "status": "success",
                "message": "User updated successfully"
            }

        except Exception:
            frappe.db.rollback()
            raise
    
    @staticmethod
    def get_user(user_id) -> dict:
        user = frappe.get_doc("User", user_id)
        if not user:
            return{
                "status": "error",
                "message": "User not found"
            }
        roles = frappe.db.get_all(
                "Has Role",
                filters = {
                    "parent": user_id,
                    "parenttype": "User",
                }, pluck = "role",
            )          
        return{
                "firstName": user.first_name,
                "lastName": user.last_name,
                "midleName": user.middle_name,
                "fullName": user.full_name,
                "email": user.email,
                "gender": user.gender,
                "username": user.username,
                "language": user.language,
                "timezone": user.time_zone,
                "dob": user.birth_date,
                "phone": user.phone,
                "mobile_no":user.mobile_no,
                "roles": roles
            }
