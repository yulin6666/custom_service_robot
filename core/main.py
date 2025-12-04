"""
客服机器人主入口
"""
import uuid
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from .graph import create_customer_service_graph
from .knowledge_base import knowledge_base
from .models import CustomerServiceState
from .log_collector import LogCollector


class CustomerServiceBot:
    """客服机器人类"""

    def __init__(self):
        """初始化机器人"""
        print("正在初始化客服机器人...")

        # 加载知识库
        print("正在加载知识库...")
        knowledge_base.load_knowledge_base()

        # 创建状态图
        print("正在创建状态图...")
        self.graph = create_customer_service_graph()

        # 会话历史
        self.sessions = {}

        print("客服机器人初始化完成！\n")

    def save_graph_to_png(self, output_path: str = "customer_service_graph.png"):
        """
        将状态图保存为PNG文件

        Args:
            output_path: 输出文件路径，默认为 "customer_service_graph.png"
        """
        try:
            # 获取图并保存为PNG
            png_data = self.graph.get_graph().draw_mermaid_png()

            with open(output_path, "wb") as f:
                f.write(png_data)

            print(f"状态图已保存到: {output_path}")
            return True
        except Exception as e:
            print(f"保存状态图时出错: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_session(self, user_id: str = None) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        if user_id is None:
            user_id = f"user_{uuid.uuid4().hex[:8]}"

        self.sessions[session_id] = {
            "user_id": user_id,
            "messages": []
        }

        return session_id

    def chat(self, user_input: str, session_id: str = None, capture_logs: bool = False) -> Dict[str, Any]:
        """
        处理用户输入并返回响应

        Args:
            user_input: 用户输入的消息
            session_id: 会话ID，如果为None则创建新会话
            capture_logs: 是否捕获并返回执行日志

        Returns:
            如果 capture_logs=False: 返回字符串响应（保持向后兼容）
            如果 capture_logs=True: 返回字典 {"response": str, "logs": List[str], "session_id": str}
        """
        # 创建日志收集器
        log_collector = None
        if capture_logs:
            log_collector = LogCollector()
            log_collector.start_capture()

        try:
            # 如果没有提供session_id，创建新会话
            if session_id is None or session_id not in self.sessions:
                session_id = self.create_session()

            # 获取会话历史
            session = self.sessions[session_id]
            user_id = session["user_id"]

            # 添加用户消息
            user_message = HumanMessage(content=user_input)
            session["messages"].append(user_message)

            # 构建初始状态
            initial_state: CustomerServiceState = {
                "messages": [user_message],
                "session_id": session_id,
                "user_id": user_id,
                "intent": None,
                "intent_confidence": None,
                "entities": None,
                "retrieved_docs": None,
                "tool_results": None,
                "need_human": False,
                "final_response": None,
                "next_step": None
            }

            # 执行状态图
            result = self.graph.invoke(initial_state)

            # 获取最终响应
            response = result.get("final_response", "抱歉，我暂时无法回答这个问题。")

            # 保存到会话历史
            session["messages"].append(HumanMessage(content=response))

            # 返回结果
            if capture_logs:
                logs = log_collector.stop_capture()
                return {
                    "response": response,
                    "logs": [log for log in logs if log.strip()],  # 过滤空行
                    "session_id": session_id,
                    "status": "success"
                }
            else:
                return response

        except Exception as e:
            print(f"处理消息时出错: {e}")
            import traceback
            traceback.print_exc()

            error_msg = "抱歉，处理您的请求时遇到了问题，请稍后再试。"

            if capture_logs:
                logs = log_collector.stop_capture() if log_collector else []
                return {
                    "response": error_msg,
                    "logs": [log for log in logs if log.strip()],
                    "session_id": session_id,
                    "status": "error",
                    "error": str(e)
                }
            else:
                return error_msg

    def run_interactive(self):
        """运行交互式命令行界面"""
        print("=" * 60)
        print("欢迎使用智能客服机器人！")
        print("=" * 60)
        print("提示：")
        print("- 输入您的问题开始对话")
        print("- 输入 'quit' 或 'exit' 退出")
        print("- 输入 'new' 开始新会话")
        print("=" * 60)
        print()

        session_id = None

        while True:
            try:
                # 获取用户输入
                user_input = input("您: ").strip()

                # 检查退出命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n感谢使用，再见！")
                    break

                # 检查新会话命令
                if user_input.lower() in ['new', '新会话']:
                    session_id = None
                    print("\n已开始新会话\n")
                    continue

                # 忽略空输入
                if not user_input:
                    continue

                # 处理消息
                response = self.chat(user_input, session_id)

                # 如果是新会话，获取session_id
                if session_id is None:
                    session_id = list(self.sessions.keys())[-1]

                # 打印响应
                print(f"\n客服: {response}\n")
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n\n感谢使用，再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {e}\n")


def main():
    """主函数"""
    bot = CustomerServiceBot()

    # 保存状态图到PNG
    bot.save_graph_to_png("customer_service_graph.png")

    bot.run_interactive()


if __name__ == "__main__":
    main()
