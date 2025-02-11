import ipywidgets as widgets
from IPython.display import display, clear_output
import asyncio

class FeedbackCollector:
    def __init__(self):
        self.feedback = None  # 初始化反馈变量
        self.future = None     # 用于异步等待用户输入
        
        # 创建下拉列表小部件
        self.feedback_widget = widgets.Dropdown(
            options=['yes', 'no', 'end'],
            value='yes',
            description='满意吗?',
            disabled=False,
        )
        
        # 创建提交按钮
        self.button = widgets.Button(description="提交反馈")
        self.button.on_click(self.on_button_clicked)
        
        # 创建输出显示结果的小部件
        self.output = widgets.Output()
        
        # 显示所有小部件
        display(self.feedback_widget, self.button, self.output)

    def on_button_clicked(self, b):
        # 当按钮被点击时，这个函数将被调用
        with self.output:
            clear_output()
            self.feedback = self.feedback_widget.value
            if self.feedback == 'yes':
                print("用户满意此计划，继续执行。")
            elif self.feedback == 'no':
                print("用户不满意此计划，需要重新调整。")
            elif self.feedback == 'end':
                print("结束反馈。")
            
            # 如果 future 存在且没有完成，则设置结果
            if self.future is not None and not self.future.done():
                self.future.set_result(self.feedback)

    async def get_feedback(self):
        """ 异步获取用户反馈 """
        self.future = asyncio.Future()  # 创建一个 future 用于等待用户输入
        await self.future  # 等待用户点击并提交反馈
        return self.future.result()  # 返回用户的反馈

# # 使用示例
async def main():
    collector = FeedbackCollector()
    feedback = await collector.get_feedback()  # 等待用户输入
    print(f"用户反馈: {feedback}")

# 运行异步函数
await main()