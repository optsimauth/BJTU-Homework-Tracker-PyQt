import os
import sys
import re
import webbrowser

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout,
                             QWidget, QPushButton, QTabWidget, QLabel, QScrollArea,
                             QGroupBox, QHBoxLayout, QGraphicsDropShadowEffect, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
import csv


class PyqtMainWindow(QMainWindow):
    def __init__(self, homework_list, display_elements=None):
        super().__init__()
        self.homework_list = self.preprocess_homework_list(homework_list)
        self.display_elements = display_elements or {
            "course_name": "课程名称",
            "title": "作业标题",
            "content": "作业说明",
            "submitCount": "已提交人数",
            "allCount": "总人数",
            "open_date": "发布日期",
            "end_time": "截止日期",
            "subStatus": "提交状态",
            # "submit_url": "提交链接"
        }
        self.initUI()

    def preprocess_homework_list(self, homework_list):
        def remove_html_tags(text):
            clean_text = re.sub(r'<.*?>', '', str(text))
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text

        return [
            {key: remove_html_tags(value) for key, value in homework.items()}
            for homework in homework_list
        ]

    def initUI(self):
        # 设置窗口基本属性
        self.setGeometry(100, 100, 1300, 850)
        self.setWindowTitle('智能作业管理中心')

        # 设置全局背景渐变
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(240, 244, 250))
        gradient.setColorAt(1, QColor(220, 230, 240))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)


        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建选项卡控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: rgba(74, 144, 226, 0.7);
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                min-width: 140px;
                margin-right: 8px;
                transition: all 0.3s ease;
            }
            QTabBar::tab:selected {
                background-color: #4A90E2;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: rgba(74, 144, 226, 0.9);
                transform: scale(1.05);
            }
        """)

        # 按课程名称分组作业
        grouped_homework = self.group_homework_by_course()

        # 为每个课程创建一个标签页
        for course_name, homeworks in grouped_homework.items():
            scroll_area = QScrollArea()
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout()
            scroll_layout.setSpacing(20)

            for homework in homeworks:
                group_box = self.create_homework_group_box(homework)
                scroll_layout.addWidget(group_box)

            scroll_layout.addStretch(1)
            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            scroll_area.setWidgetResizable(True)

            # 将滚动区域添加到标签页
            self.tab_widget.addTab(scroll_area, course_name)

        # 创建底部按钮布局
        button_layout = QHBoxLayout()

        # 导出按钮
        export_button = QPushButton('导出作业')
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #27AE60;
                transform: scale(1.05);
            }
        """)
        export_button.clicked.connect(self.export_homework)

        # 关闭按钮
        close_button = QPushButton('关闭')
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #FF4757;
                transform: scale(1.05);
            }
        """)
        close_button.clicked.connect(self.close)

        # 添加控件到布局
        button_layout.addWidget(export_button)
        button_layout.addWidget(close_button)

        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

    def group_homework_by_course(self):
        grouped = {}
        for homework in self.homework_list:
            course_name = homework.get('course_name', '其他')
            grouped.setdefault(course_name, []).append(homework)
        return grouped

    def create_homework_group_box(self, homework):
        group_box = QGroupBox()
        group_box.setStyleSheet("""
            QGroupBox {
                border: none;
                border-radius: 20px;
                background-color: white;
                margin-top: 15px;
                padding: 20px;
                transition: all 0.3s ease;
            }
            QGroupBox:hover {
                transform: translateY(-5px);
            }
        """)

        # 阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 7)
        group_box.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # 标题栏
        title_label = QLabel(homework.get('title', '未命名作业'))
        title_label.setFont(QFont('微软雅黑', 14, QFont.Bold))
        title_label.setStyleSheet("""
            color: #2C3E50;
            padding-bottom: 10px;
            border-bottom: 2px solid #4A90E2;
        """)
        layout.addWidget(title_label)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 提交链接按钮
        submit_url = homework.get('submit_url', '')
        if submit_url:
            submit_button = QPushButton('打开提交链接')
            submit_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
            """)
            submit_button.clicked.connect(lambda: self.open_submit_link(submit_url))
            button_layout.addWidget(submit_button)

        # 下载附件按钮（如果有附件）
        attachment = homework.get('attachment', '')
        if attachment:
            download_button = QPushButton('下载附件')
            download_button.setStyleSheet("""
                QPushButton {
                    background-color: #2ECC71;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
            """)
            download_button.clicked.connect(lambda: self.download_attachment(attachment))
            button_layout.addWidget(download_button)

        # 添加按钮布局
        layout.addLayout(button_layout)

        # 遍历display_elements中的字段
        for key, display_name in self.display_elements.items():
            if key not in ['submit_url', 'attachment']:
                value = homework.get(key, '')
                if value:  # 只显示非空的信息
                    label = QLabel(f"{display_name}: {value}")
                    label.setFont(QFont('微软雅黑', 10))
                    label.setStyleSheet("""
                        color: #34495E;
                        padding: 6px 10px;
                        border-bottom: 1px solid #ECF0F1;
                    """)
                    label.setWordWrap(True)
                    layout.addWidget(label)

        group_box.setLayout(layout)
        return group_box

    def export_homework(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "导出作业信息", "", "文本文件 (*.txt);;Excel文件 (*.csv)")

            if file_path:
                file_extension = os.path.splitext(file_path)[1].lower()

                if file_extension == '.txt':
                    self.export_to_txt(file_path)
                elif file_extension == '.csv':
                    self.export_to_csv(file_path)

                QMessageBox.information(self, "导出成功", f"作业信息已成功导出到 {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出过程中发生错误: {str(e)}")

    def export_to_txt(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            for homework in self.homework_list:
                f.write("=" * 50 + "\n")
                for key, display_name in self.display_elements.items():
                    value = homework.get(key, '')
                    if value:
                        f.write(f"{display_name}: {value}\n")
                f.write("=" * 50 + "\n\n")

    def export_to_csv(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入标题行
            headers = [display_name for display_name in self.display_elements.values()]
            writer.writerow(headers)

            # 写入数据
            for homework in self.homework_list:
                row = [homework.get(key, '') for key in self.display_elements.keys()]
                writer.writerow(row)

    def open_submit_link(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self, "打开链接失败", f"无法打开链接: {str(e)}")

    def download_attachment(self, attachment_url):
        try:
            # 选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(self, "保存附件", "", "All Files (*.*)")

            if file_path:
                # 这里应该添加实际的下载逻辑
                # 可以使用 requests 库下载附件
                QMessageBox.warning(self, "提示", "请实现具体的下载逻辑")
        except Exception as e:
            QMessageBox.warning(self, "下载失败", f"下载附件时发生错误: {str(e)}")


def show_homework_window(homework_list: list, display_elements=None):
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用更现代的界面风格
    main_window = PyqtMainWindow(homework_list, display_elements)
    main_window.show()
    sys.exit(app.exec_())


# 使用示例
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
    show_homework_window(homework_list,display_elements)