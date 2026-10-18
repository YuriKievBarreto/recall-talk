from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.repositories.user_repository import UserRepository

from app.core.database import get_session


from fastapi import Depends
from sqlmodel import Session

def get_user_repository(session: Session = Depends(get_session)) -> IUserRepository:
    return UserRepository(session=session)
