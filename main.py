import asyncio
import warnings
from config import FILE_PATH, XIAOAI_URL
from defs.wakeup import WakeUp
from defs.xiaoai import XiaoAi

warnings.filterwarnings("ignore", category=DeprecationWarning)


async def main():
    wakeup = WakeUp(FILE_PATH)
    xiaoai = XiaoAi(XIAOAI_URL)
    print(f"链接过期时间：{xiaoai.expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
    wakeup.load_data()
    data = wakeup.convert_data()
    table = await xiaoai.get_all_course()
    print(f"开始处理课程表 - {table.name}")
    print("开始删除课程表数据")
    await xiaoai.delete_all_course()
    print("开始导入课程表数据")
    for i in data:
        await xiaoai.add_course(i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
