from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.conf import constants
from src.conf import messages

class ContactBookSchema(BaseModel):
    name: str = Field(min_length=constants.USER_NAME_MIN_LENGTH, max_length=constants.USER_NAME_MAX_LENGTH)
    surname: str = Field(min_length=constants.USER_SURNAME_MIN_LENGTH, max_length=constants.USER_SURNAME_MAX_LENGTH)
    email: EmailStr
    phone: str
    date_of_birth: datetime

class ContactBookUpdateSchema(BaseModel):
    name: Optional[str] = Field(min_length=constants.USER_NAME_MIN_LENGTH, max_length=constants.USER_NAME_MAX_LENGTH)
    surname: Optional[str] = Field(min_length=constants.USER_SURNAME_MIN_LENGTH, max_length=constants.USER_SURNAME_MAX_LENGTH)
    email: Optional[EmailStr]
    phone: Optional[str]
    date_of_birth: Optional[datetime]

class ContactBookResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: str
    date_of_birth: datetime

    model_config = ConfigDict(from_attributes=True)