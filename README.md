# BJTU-Homework-Tracker-PyQt
这是一个GUI界面

## 使用示例
```python
if __name__ == '__main__':
    homework_list = [
        {
            "course_name": "数学",
            "title": "数学作业",
            "content": "解答习题1-10",
            "submitCount": "20",
            "allCount": "30",
            "open_date": "2024-01-01",
            "end_time": "2024-02-15",
            "subStatus": "未提交"
        },
        {
            "course_name": "英语",
            "title": "英语作业",
            "content": "阅读理解",
            "submitCount": "15",
            "allCount": "30",
            "open_date": "2024-01-15",
            "end_time": "2024-02-20",
            "subStatus": "已提交",
        },
        {
            "course_name": "数学",
            "title": "数学作业",
            "content": "阅读理解",
            "submitCount": "15",
            "allCount": "30",
            "open_date": "2024-01-15",
            "end_time": "2024-02-20",
            "subStatus": "已提交",
        }
    ]
    display_elements ={
                "course_name": "课程名称",
                "title": "作业标题",
                "content": "作业说明",
                "submitCount": "已提交人数",
                "allCount": "总人数",
                "open_date": "发布日期",
                "end_time": "截止日期",
                "subStatus": "提交状态",
                "submit_url": "提交链接"
    }
    show_homework_window(homework_list,display_elements)

"""
全部的display_elements
display_elements = {
    "id": "作业ID",
    "create_date": "创建日期",
    "course_id": "课程ID",
    "course_sched_id": "课程安排ID",
    "course_name": "课程名称",
    "comment_num": "评论数",
    "content": "作业内容",
    "title": "作业标题",
    "user_id": "用户ID",
    "praise_num": "点赞数",
    "is_fz": "是否分组",
    "content_type": "内容类型",
    "calendar_id": "日历ID",
    "end_time": "截止日期",
    "open_date": "发布日期",
    "score": "总分",
    "moudel_id": "模块ID",
    "isOpen": "是否公开",
    "status": "状态",
    "submitCount": "已提交人数",
    "allCount": "总人数",
    "excellentCount": "优秀作业数",
    "is_publish_answer": "是否发布答案",
    "review_method": "批改方式",
    "makeup_flag": "补交标志",
    "is_repeat": "是否重复提交",
    "makeup_time": "补交时间",
    "snId": "序列ID",
    "scoreId": "成绩ID",
    "subTime": "提交时间",
    "subStatus": "提交状态",
    "return_flag": "退回标志",
    "return_num": "退回次数",
    "is_excellent": "是否优秀",
    "stu_score": "学生成绩",
    "refAnswer": "参考答案",
    "pg_user_id": "批改用户ID",
    "pg_user_name": "批改用户名",
    "returnContent": "退回内容",
    "lastScore": "最终成绩"
}
"""


```




效果展示:
![](https://s2.loli.net/2024/11/28/uUMbSvEPdtXi2hx.png)



