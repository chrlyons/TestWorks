from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    name: str


class ReportBase(BaseModel):
    name: str


class ReportCreate(ReportBase):
    data: str


class Report(ReportBase):
    id: int


class ReportSchema(BaseModel):
    id: int
    name: str
    data: str
