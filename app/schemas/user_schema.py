from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)
    confirm_password: str = Field(..., alias="confirm password")
    name: Optional[str] = None
    role: Optional[int] = 0
    condition: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None

    @model_validator(mode='after')
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, max_length=72)
    name: Optional[str] = None
    role: Optional[int] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    role: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
