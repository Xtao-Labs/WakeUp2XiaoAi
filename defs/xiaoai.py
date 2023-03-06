import base64
import re
from datetime import datetime
from typing import Dict
from httpx import AsyncClient
from models.xiaoai import AiCourse, AiCourseInfo, Table, TabCourse


class XiaoAi:
    HEADERS = {
        'authority': 'i.ai.mi.com',
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,hu;q=0.5',
        'access-control-allow-origin': 'true',
        'content-type': 'application/json',
        'origin': 'https://i.ai.mi.com',
        'referer': 'https://i.ai.mi.com/h5/precache/ai-schedule/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    }
    URL = "https://i.ai.mi.com/course-multi/courseInfo"
    TABLE_URL = "https://i.ai.mi.com/course-multi/table"

    def __init__(self, url_temp: str) -> None:
        while True:
            url = url_temp or input("请输入包含 token 的小爱课程表链接 : ")
            token = re.search(r"token=(.*)", url)
            if not token:
                print("链接错误, 请重新输入。")
                url_temp = None
                continue
            decoded_text = base64.b64decode(token[1]).decode('utf-8').split("%26")
            self.user_id = int(decoded_text[0])
            self.device_id = decoded_text[1]
            timestamp = int(decoded_text[2]) / 1000
            self.expire_time = datetime.fromtimestamp(timestamp)
            self.ct_id = int(decoded_text[3])
            break
        self.client: AsyncClient = AsyncClient(headers=self.HEADERS)
        self.table: Table = None

    async def get_all_course(self) -> Table:
        """ 获取课程表数据 """
        params = {
            'ctId': str(self.ct_id),
            'userId': str(self.user_id),
            'deviceId': self.device_id,
            'sourceName': 'course-app-browser',
        }
        data = await self.client.get(self.TABLE_URL, params=params)
        json_data = data.json()
        if json_data["code"] != 0:
            raise ValueError("课程表不存在或者链接已过期")
        self.table = Table(**json_data["data"])
        return self.table

    async def delete_course(self, course: TabCourse) -> None:
        """ 删除某个课程 """
        json_data = {
            'ctId': self.ct_id,
            'userId': self.user_id,
            'deviceId': self.device_id,
            'cId': course.id,
            'sourceName': 'course-app-browser',
        }
        await self.client.request("DELETE", self.URL, json=json_data)

    async def delete_all_course(self) -> None:
        """ 删除课程表数据 """
        for i in self.table.courses:
            await self.delete_course(i)

    async def add_course(self, course: AiCourse) -> None:
        """ 添加课程 """
        info = AiCourseInfo(userId=self.user_id, deviceId=self.device_id, ctId=self.ct_id, course=course)
        await self.client.post(self.URL, json=info.dict())
