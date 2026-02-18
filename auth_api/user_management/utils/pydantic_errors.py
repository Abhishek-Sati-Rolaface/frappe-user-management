from pydantic import ValidationError

def format_pydantic_errors(exc: ValidationError):
    errors = {}

    for err in exc.errors():
        field = err["loc"][0] if err.get("loc") else "unknown"
        message = err.get("msg")

        if err["type"] == "missing":
            message = f"{field} is required"

        errors[field] = message

    return errors
