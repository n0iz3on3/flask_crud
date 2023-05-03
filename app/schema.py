import re
from pydantic import BaseModel, EmailStr, ValidationError, validator
from typing import Any, Dict, Optional, Type

from errors import HttpError
from config import PASSWORD_LENGTH


PASSWORD_REGEX = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])*.{{{password_length},}}$".format(
        password_length=PASSWORD_LENGTH
    )
)


class Register(BaseModel):

    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value: str):
        if not PASSWORD_REGEX.match(value):
            raise ValueError('password is to easy')
        return value


class Login(BaseModel):

    email: EmailStr
    password: str


class PatchUser(BaseModel):

    email: Optional[EmailStr]
    password: Optional[str]


class CreateAds(BaseModel):

    title: str
    description: str

    @validator('title')
    def validate_title(cls, value: str):
        if not (5 <= value <= 35):
            raise ValueError('incorrect title length')
        return value

    @validator('description')
    def validate_description(cls, value: str):
        if value > 120:
            raise ValueError('description character limit exceeded')
        return


class PatchAds(CreateAds, BaseModel):

    title: Optional[str]
    description: Optional[str]


SCHEMA_TYPE = Type[Register] | Type[Login] | Type[PatchUser] | Type[PatchAds] | Type[CreateAds]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated
