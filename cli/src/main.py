import os
import requests

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8001/query")

def main():
    print(f"Connecting to orchestrator at {ORCHESTRATOR_URL}")
    print("Type your question or 'exit' to quit.")
    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue

        try:
            response = requests.post(ORCHESTRATOR_URL, json={"question": question})
            response.raise_for_status()
            data = response.json()
            print("\nResponse:\n" + data.get("response", "No response"))
        except requests.RequestException as e:
            print(f"Error communicating with orchestrator: {e}")

if __name__ == "__main__":
    main()
