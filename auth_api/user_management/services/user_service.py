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
    def get_users(page=1, page_size=10, search="", filters=None):

        filters = filters or {}
        limit_start = (page - 1) * page_size

        users = UserRepository.get_users(
            filters=filters,
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