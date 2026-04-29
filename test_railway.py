"""
Railway Deployment Test Script
Used to test the customer service bot REST API deployed on Railway
"""
import requests
import json
import sys


# Railway deployment domain
BASE_URL = "https://customservicerobot-production.up.railway.app"


def print_section(title):
    """Print separator line"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health_check():
    """Test health check"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_create_session():
    """Test session creation"""
    print_section("2. Create Session")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/sessions",
            json={"user_id": "test_user_123"},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return data.get("session_id")
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_chat(session_id, message):
    """Test chat"""
    print_section(f"Chat Test: \"{message}\"")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=60  # Chat may take longer
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()

        # Print response
        print(f"\n【Bot Reply】\n{data.get('response')}\n")

        # Print execution logs
        print("【LangGraph Execution Logs】")
        logs = data.get('logs', [])
        for log in logs:
            if log.strip():  # Skip empty lines
                print(log)

        print(f"\nSession ID: {data.get('session_id')}")
        print(f"Status: {data.get('status')}")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Content: {e.response.text}")
        return False


def test_get_graph():
    """Test getting state graph"""
    print_section("Get State Graph")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph", timeout=30)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            # Save image
            with open("railway_graph.png", "wb") as f:
                f.write(response.content)
            print("✅ State graph saved to railway_graph.png")
            return True
        else:
            print(f"❌ Failed to get: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main test flow"""
    print("\n" + "🚀" * 30)
    print("  Railway Deployment Test")
    print(f"  Domain: {BASE_URL}")
    print("🚀" * 30)

    # 1. Health check
    print("\nTesting service health status...")
    if not test_health_check():
        print("\n❌ Health check failed, please check:")
        print("1. Is the service successfully deployed")
        print("2. Is the domain correct")
        print("3. Check Railway logs to troubleshoot")
        sys.exit(1)

    print("\n✅ Service is running normally!")

    # 2. Create session
    session_id = test_create_session()
    if not session_id:
        print("\n❌ Failed to create session")
        sys.exit(1)

    # 3. Test multi-turn conversation
    test_messages = [
        "Hello",
        "What is the return process?",
        "I want to check order ORD001"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}/{len(test_messages)}] Test message: {message}")
        if not test_chat(session_id, message):
            print(f"\n❌ Chat test failed: {message}")
            break

    # 4. Get state graph
    test_get_graph()

    print_section("Test Complete")
    print("✅ All tests completed!")
    print("\n📝 Tips:")
    print("- View railway_graph.png to see the state graph")
    print("- Check the logs above to understand LangGraph execution process")
    print(f"- Visit {BASE_URL}/docs to view complete API documentation")
    print(f"- Open {BASE_URL}/api/v1/graph in browser to view state graph")


if __name__ == "__main__":
    main()
