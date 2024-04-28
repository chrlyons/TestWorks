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

    class Config:
        from_attributes = True


class ReportSchema(BaseModel):
    id: int
    name: str
    data: str

    class Config:
        from_attributes = True
