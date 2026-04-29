"""
API test script
For quickly testing the customer service bot REST API
"""
import requests
import json
import sys


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print separator line"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health_check():
    """Test health check"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_create_session():
    """Test session creation"""
    print_section("2. Create Session")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/sessions",
            json={"user_id": "test_user_123"}
        )
        print(f"Status code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return data.get("session_id")
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_chat(session_id, message):
    """Test chat"""
    print_section(f"3. Chat Test: \"{message}\"")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        print(f"Status code: {response.status_code}")
        data = response.json()

        # Print response
        print(f"\n[Bot Reply]\n{data.get('response')}\n")

        # Print execution logs
        print("[LangGraph Execution Logs]")
        logs = data.get('logs', [])
        for log in logs:
            if log.strip():  # Skip empty lines
                print(log)

        print(f"\nSession ID: {data.get('session_id')}")
        print(f"Status: {data.get('status')}")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_graph():
    """Test get state graph"""
    print_section("4. Get State Graph")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph")
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            # Save image
            with open("test_graph.png", "wb") as f:
                f.write(response.content)
            print("State graph saved to test_graph.png")
            return True
        else:
            print(f"Failed to get graph: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Main test flow"""
    print("\n" + "🤖" * 30)
    print("  Intelligent Customer Service Bot API Test")
    print("🤖" * 30)

    # 1. Health check
    if not test_health_check():
        print("\nHealth check failed. Please ensure the service is running.")
        sys.exit(1)

    # 2. Create session
    session_id = test_create_session()
    if not session_id:
        print("\nFailed to create session")
        sys.exit(1)

    # 3. Test multi-turn conversation
    test_messages = [
        "Hello",
        "What is the return process?",
        "I want to check order ORD001"
    ]

    for message in test_messages:
        if not test_chat(session_id, message):
            print(f"\nChat test failed: {message}")
            break

    # 4. Get state graph
    test_get_graph()

    print_section("Test Complete")
    print("All tests completed!")
    print("\nTips:")
    print("- View test_graph.png to see the state graph")
    print("- Check the logs above to understand the LangGraph execution process")
    print("- Visit http://localhost:8000/docs for complete API documentation")


if __name__ == "__main__":
    main()
