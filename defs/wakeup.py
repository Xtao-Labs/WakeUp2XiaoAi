import json
from pathlib import Path
from typing import Dict, List
from models.wakeup import Course, CourseInfo
from models.xiaoai import AiCourse


class WakeUp:
    def __init__(self, file_path: str) -> None:
        while True:
            self.file_path = file_path or input("请输入文件路径 (例如 test.wakeup_schedule ): ")
            path = Path(self.file_path)
            if not path.exists():
                print("文件不存在, 请重新输入路径.")
                file_path = None
                continue
            break
        self.old_data: List[Course] = []
        self.old_data_info: List[CourseInfo] = []
        self.old_data_info_map: Dict[int, CourseInfo] = {}
        self.weeks_map: Dict[str, List[int]] = {}
        self.new_data: List[AiCourse] = []
        self.new_data_map: Dict[str, List[AiCourse]] = {}

    def load_data(self) -> None:
        """ 解析 wakeup 备份文件数据 """
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.old_data_info = [CourseInfo(**i) for i in json.loads(lines[3])]
        for i in self.old_data_info:
            self.old_data_info_map[i.id] = i
        self.old_data = [Course(**i) for i in json.loads(lines[4])]
        for i in self.old_data:
            data = self.weeks_map.get(i.key, [].copy())
            data.extend(i.weeks)
            self.weeks_map[i.key] = data
        # 移除重复 id
        temp_keys, old_data = [], []
        for i in self.old_data:
            if i.key in temp_keys:
                continue
            old_data.append(i)
            temp_keys.append(i.key)
        self.old_data = old_data
    
    def get_weeks(self, temp: Course) -> str:
        """ 获取当前课程周数 """
        return ",".join(list(map(str, self.weeks_map[temp.key])))

    def convert_data(self) -> List[AiCourse]:
        """ 转换为小爱课程表格式 """
        for i in self.old_data:
            old_data_info = self.old_data_info_map[i.id]
            self.new_data.append(
                AiCourse(
                    name=old_data_info.courseName,
                    position=i.room,
                    teacher=i.teacher,
                    weeks=self.get_weeks(i),
                    day=i.day,
                    style=old_data_info.style,
                    sections=i.sections,
                )
            )
        return self.new_data
