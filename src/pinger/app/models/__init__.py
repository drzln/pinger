from pydantic import BaseModel


class Report(BaseModel):
    title: str
    content: str


class ReportOut(Report):
    id: str
