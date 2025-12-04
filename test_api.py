"""
API 测试脚本
用于快速测试客服机器人 REST API
"""
import requests
import json
import sys


BASE_URL = "http://localhost:8000"


def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health_check():
    """测试健康检查"""
    print_section("1. 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_create_session():
    """测试创建会话"""
    print_section("2. 创建会话")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/sessions",
            json={"user_id": "test_user_123"}
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return data.get("session_id")
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def test_chat(session_id, message):
    """测试对话"""
    print_section(f"3. 对话测试: \"{message}\"")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        print(f"状态码: {response.status_code}")
        data = response.json()

        # 打印响应
        print(f"\n【机器人回复】\n{data.get('response')}\n")

        # 打印执行日志
        print("【LangGraph 执行日志】")
        logs = data.get('logs', [])
        for log in logs:
            if log.strip():  # 跳过空行
                print(log)

        print(f"\n会话ID: {data.get('session_id')}")
        print(f"状态: {data.get('status')}")

        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_get_graph():
    """测试获取状态图"""
    print_section("4. 获取状态图")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph")
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            # 保存图片
            with open("test_graph.png", "wb") as f:
                f.write(response.content)
            print("✅ 状态图已保存到 test_graph.png")
            return True
        else:
            print(f"❌ 获取失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    """主测试流程"""
    print("\n" + "🤖" * 30)
    print("  智能客服机器人 API 测试")
    print("🤖" * 30)

    # 1. 健康检查
    if not test_health_check():
        print("\n❌ 健康检查失败，请确保服务已启动")
        sys.exit(1)

    # 2. 创建会话
    session_id = test_create_session()
    if not session_id:
        print("\n❌ 创建会话失败")
        sys.exit(1)

    # 3. 测试多轮对话
    test_messages = [
        "你好",
        "退货流程是什么？",
        "我想查询订单ORD001"
    ]

    for message in test_messages:
        if not test_chat(session_id, message):
            print(f"\n❌ 对话测试失败: {message}")
            break

    # 4. 获取状态图
    test_get_graph()

    print_section("测试完成")
    print("✅ 所有测试已完成！")
    print("\n提示：")
    print("- 查看 test_graph.png 了解状态图")
    print("- 查看上面的日志了解 LangGraph 执行过程")
    print("- 访问 http://localhost:8000/docs 查看完整 API 文档")


if __name__ == "__main__":
    main()
