from typing import List
from pydantic import BaseModel


class AiCourse(BaseModel):
    name: str
    position: str
    teacher: str
    weeks: str
    day: int
    style: str
    sections: str


class TabCourse(AiCourse):
    id: int


class AiCourseInfo(BaseModel):
    userId: int
    deviceId: str
    ctId: int
    course: AiCourse
    sourceName: str = "course-app-browser"


class Table(BaseModel):
    id: int
    name: str
    courses: List[TabCourse]
