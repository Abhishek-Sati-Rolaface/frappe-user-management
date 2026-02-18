from auth_api.user_management.repositories.user_repo import UserRepository
import frappe
class UserService:

    @staticmethod
    def signup(payload: dict) -> dict:
        try:
            frappe.db.begin()

            user = UserRepository.create_user(payload)
            
            frappe.db.commit()

            return {
                "status": "success",
                "message": "User created successfully, Please check your email for login credentials"
            }

        except Exception:
            frappe.db.rollback()
            raise
