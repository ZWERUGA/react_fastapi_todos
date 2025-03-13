from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserDB(UserBase):
    hashed_password: str
