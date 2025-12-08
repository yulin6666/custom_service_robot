"""
Railway 部署测试脚本
用于测试部署在 Railway 上的客服机器人 REST API
"""
import requests
import json
import sys


# Railway 部署的域名
BASE_URL = "https://customservicerobot-production.up.railway.app"


def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health_check():
    """测试健康检查"""
    print_section("1. 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
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
            json={"user_id": "test_user_123"},
            timeout=30
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
    print_section(f"对话测试: \"{message}\"")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=60  # 对话可能需要更长时间
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
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}")
        return False


def test_get_graph():
    """测试获取状态图"""
    print_section("获取状态图")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph", timeout=30)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            # 保存图片
            with open("railway_graph.png", "wb") as f:
                f.write(response.content)
            print("✅ 状态图已保存到 railway_graph.png")
            return True
        else:
            print(f"❌ 获取失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    """主测试流程"""
    print("\n" + "🚀" * 30)
    print("  Railway 部署测试")
    print(f"  域名: {BASE_URL}")
    print("🚀" * 30)

    # 1. 健康检查
    print("\n正在测试服务健康状态...")
    if not test_health_check():
        print("\n❌ 健康检查失败，请检查：")
        print("1. 服务是否已成功部署")
        print("2. 域名是否正确")
        print("3. 查看 Railway 日志排查问题")
        sys.exit(1)

    print("\n✅ 服务运行正常！")

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

    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}/{len(test_messages)}] 测试消息: {message}")
        if not test_chat(session_id, message):
            print(f"\n❌ 对话测试失败: {message}")
            break

    # 4. 获取状态图
    test_get_graph()

    print_section("测试完成")
    print("✅ 所有测试已完成！")
    print("\n📝 提示：")
    print("- 查看 railway_graph.png 了解状态图")
    print("- 查看上面的日志了解 LangGraph 执行过程")
    print(f"- 访问 {BASE_URL}/docs 查看完整 API 文档")
    print(f"- 在浏览器中打开 {BASE_URL}/api/v1/graph 查看状态图")


if __name__ == "__main__":
    main()
