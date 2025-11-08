import easygui as eg
import json
import os
from volcenginesdkarkruntime import Ark
#请自行填写API，采用火山方舟模型
os.environ['ARK_API_KEY'] = ''
class SimpleAIChat:
    def __init__(self):
        self.conversation_history = []
        
    def call_ai_api(self, user_input):
        """
        在这里实现您的API调用逻辑
        这是一个示例，您需要根据实际API进行调整
        """
        try:
            client = Ark(
                # 此为默认路径，您可根据业务所在地域进行配置
                base_url="https://ark.cn-beijing.volces.com/api/v3",
                # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
                api_key=os.environ.get("ARK_API_KEY"),
            )
            completion = client.chat.completions.create(
               # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
                model="deepseek-v3-1-terminus",
                messages=[
                    {"role": "system", "content": "你是人工智能助手."},
                    {"role": "user", "content": "你好"},
                ],
                # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
                extra_headers={'x-is-encrypted': 'true'},
            )
            return(completion.choices[0].message.content)
                
        except Exception as e:
            return f"发生错误：{str(e)}"
    
    def start_chat(self):
        """启动AI聊天界面"""
        eg.msgbox("欢迎使用AI聊天助手！", "AI助手")
        
        while True:
            # 获取用户输入
            user_input = eg.enterbox(
                "请输入您的问题：", 
                "AI聊天助手",
                ""
            )
            
            # 检查用户是否取消或关闭窗口
            if user_input is None:
                if eg.ccbox("确定要退出聊天吗？", "退出确认"):
                    break
                else:
                    continue
            
            # 检查输入是否为空
            if not user_input.strip():
                eg.msgbox("输入不能为空，请重新输入！", "提示")
                continue
            
            # 显示处理中消息
            eg.msgbox("AI正在思考中，请稍候...", "处理中")
            
            # 调用API
            ai_response = self.call_ai_api(user_input)
            
            # 保存对话记录
            self.conversation_history.append({
                "question": user_input,
                "answer": ai_response
            })
            
            # 显示AI回复
            self.show_response(user_input, ai_response)
    
    def show_response(self, question, answer):
        """显示AI回复的界面"""
        # 格式化显示内容
        display_text = f"❓ 您的提问：{question}\n\n"
        display_text += f"🤖 AI回复：{answer}\n\n"
        display_text += "=" * 50
        
        # 显示回复并提供操作选项
        eg.textbox("AI回复", "对话结果", display_text)
        
        # 询问下一步操作
        choices = ["继续提问", "查看历史", "退出"]
        next_action = eg.buttonbox("请选择下一步操作：", "继续聊天", choices)
        
        if next_action == "查看历史":
            self.show_history()
        elif next_action == "退出":
            if eg.ccbox("确定要退出吗？", "退出确认"):
                return "exit"
    
    def show_history(self):
        """显示对话历史"""
        if not self.conversation_history:
            eg.msgbox("暂无对话记录！", "历史记录")
            return
        
        # 格式化历史记录
        history_text = "📚 对话历史记录\n\n"
        for i, chat in enumerate(self.conversation_history, 1):
            history_text += f"{i}. 问：{chat['question']}\n"
            history_text += f"   答：{chat['answer']}\n"
            history_text += "-" * 40 + "\n"
        
        # 显示历史记录
        eg.textbox("对话历史", "历史记录", history_text)
        
        # 历史记录操作
        if self.conversation_history:
            if eg.ynbox("是否要清空历史记录？", "清空记录"):
                self.conversation_history = []
                eg.msgbox("历史记录已清空！", "完成")

def main():
    """主函数"""
    # 创建聊天实例
    chat_bot = SimpleAIChat()
    
    # 显示主界面
    eg.msgbox("""
    🚀 AI助手已启动！
    采用deepseek模型
    
    功能说明：
    • 在输入框中输入您的问题
    • 点击OK发送给AI
    • 查看AI的回复
    • 支持对话历史记录
    
    点击确定开始使用！
    """, "AI聊天助手")
    
    # 开始聊天
    chat_bot.start_chat()
    
    # 退出提示
    eg.msgbox("感谢使用AI聊天助手！", "再见")

if __name__ == "__main__":
    main()
