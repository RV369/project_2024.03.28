import uuid
from datetime import date

from sqlmodel import Field, SQLModel


class NameFile(SQLModel):
    pass


class UploadedFile(NameFile, table=True):
    uid: str = Field(uuid.UUID, primary_key=True)
    filename: str
    upload_date: date
