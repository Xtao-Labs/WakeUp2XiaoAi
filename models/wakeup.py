from typing import List
from pydantic import BaseModel


class Course(BaseModel):
    id: int
    day: int  # 周几
    startWeek: int  # 开始的周次
    endWeek: int  # 停止的周次
    startNode: int  # 开始的节次
    step: int  # 有多少节
    room: str  # 位置
    teacher: str  # 老师

    @property
    def sections(self) -> str:
        data = map(str, list(range(self.startNode, self.startNode + self.step)))
        return ",".join(data)

    @property
    def key(self) -> str:
        return f"{self.id}_{self.day}_{self.startNode}_{self.step}"

    @property
    def weeks(self) -> List[int]:
        return list(range(self.startWeek, self.endWeek + 1))


class CourseInfo(BaseModel):
    id: int
    color: str
    courseName: str

    @property
    def style(self) -> str:
        return '{"color":"#FFFFFF", "background":"#' + self.color[3:] + '"}'
