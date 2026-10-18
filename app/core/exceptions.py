from fastapi import HTTPException, status


class EmailAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User with this email already exists.") -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Invalid email or password.") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

