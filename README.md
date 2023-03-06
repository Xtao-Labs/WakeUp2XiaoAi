# WakeUp2XiaoAi

A python script to convert WakeUp json to Xiao Ai Schedule.

将 WakeUp 课程表的数据导入到小爱课程表，解决小爱课程表教务导入过于破烂的问题

# 使用方法

## 导出课程表

将 WakeUp 中已经导入好的课程表使用右上方分享按钮 `导出为备份（可导入）文件` 放置于 `main.py` 同目录下，假设此文件名称为：`test.wakeup_schedule`

## 建立课程表

在小爱课程表建立一个课程表，设置好上课时间、总周数、课程节数、课表时间

## 导出编辑链接

在建好的课程表设置页，选择 `PC编辑课表` 导出编辑链接，然后复制链接，假设此链接为：`https://i.ai.mi.com/h5/precache/ai-schedule/#/pceditor?token=1`

## 运行脚本

`python3 main.py`

然后输入 `test.wakeup_schedule`

然后输入 `https://i.ai.mi.com/h5/precache/ai-schedule/#/pceditor?token=1`

回到小爱课程表，发现同步完成。
