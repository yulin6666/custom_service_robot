"""
Main entry point for the internal enterprise query assistant
"""
import uuid
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from .graph import create_enterprise_query_graph
from .knowledge_base import knowledge_base
from .models import EnterpriseQueryState
from .log_collector import LogCollector


class EnterpriseQueryBot:
    """Internal enterprise query assistant class"""

    def __init__(self):
        """Initialize the query assistant"""
        print("Initializing internal enterprise query assistant...")

        # Load knowledge base
        print("Loading knowledge base...")
        knowledge_base.load_knowledge_base()

        # Create state graph
        print("Creating state graph...")
        self.graph = create_enterprise_query_graph()

        # Session history
        self.sessions = {}

        print("Internal enterprise query assistant initialization complete!\n")

    def save_graph_to_png(self, output_path: str = "customer_service_graph.png"):
        """
        Save the state graph as a PNG file

        Args:
            output_path: Output file path, default is "customer_service_graph.png"
        """
        try:
            # Get graph and save as PNG
            png_data = self.graph.get_graph().draw_mermaid_png()

            with open(output_path, "wb") as f:
                f.write(png_data)

            print(f"State graph saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving state graph: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_session(self, user_id: str = None) -> str:
        """Create a new session"""
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
        Process user input and return response

        Args:
            user_input: User input message
            session_id: Session ID; if None, creates a new session
            capture_logs: Whether to capture and return execution logs

        Returns:
            If capture_logs=False: returns string response (backward compatible)
            If capture_logs=True: returns dict {"response": str, "logs": List[str], "session_id": str}
        """
        # Create log collector
        log_collector = None
        if capture_logs:
            log_collector = LogCollector()
            log_collector.start_capture()

        try:
            # Create new session if session_id is not provided
            if session_id is None or session_id not in self.sessions:
                session_id = self.create_session()

            # Get session history
            session = self.sessions[session_id]
            user_id = session["user_id"]

            # Add user message
            user_message = HumanMessage(content=user_input)
            session["messages"].append(user_message)

            # Build initial state
            initial_state: EnterpriseQueryState = {
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

            # Execute state graph
            result = self.graph.invoke(initial_state)

            # Get final response
            response = result.get("final_response", "Sorry, I cannot answer this question right now.")

            # Save to session history
            session["messages"].append(HumanMessage(content=response))

            # Return result
            if capture_logs:
                logs = log_collector.stop_capture()
                return {
                    "response": response,
                    "logs": [log for log in logs if log.strip()],
                    "session_id": session_id,
                    "status": "success"
                }
            else:
                return response

        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()

            error_msg = "Sorry, there was an issue processing your request. Please try again later."

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
        """Run interactive command-line interface"""
        print("=" * 60)
        print("Welcome to the internal enterprise query assistant!")
        print("=" * 60)
        print("Tips:")
        print("- Enter your question to start chatting")
        print("- Enter 'quit' or 'exit' to leave")
        print("- Enter 'new' to start a new session")
        print("=" * 60)
        print()

        session_id = None

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Check exit command
                if user_input.lower() in ['quit', 'exit']:
                    print("\nThanks for using the assistant. Goodbye!")
                    break

                # Check new session command
                if user_input.lower() in ['new', 'new session']:
                    session_id = None
                    print("\nNew session started\n")
                    continue

                # Ignore empty input
                if not user_input:
                    continue

                # Process message
                response = self.chat(user_input, session_id)

                # Get session_id for new session
                if session_id is None:
                    session_id = list(self.sessions.keys())[-1]

                # Print response
                print(f"\nAssistant: {response}\n")
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n\nThanks for using the assistant. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")


def main():
    """Main function"""
    bot = EnterpriseQueryBot()

    # Save state graph to PNG
    bot.save_graph_to_png("customer_service_graph.png")

    bot.run_interactive()


if __name__ == "__main__":
    main()
