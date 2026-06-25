from database.postgres import init_db
from agents.orchestrator import Orchestrator
from core.event_bus import event_bus
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Initializing Database...")
    init_db()
    
    print("Initializing Orchestrator...")
    orchestrator = Orchestrator()
    
    #user session
    print("\n--- Starting Session ---")
    customer_id = "cust_001"
    session_id = orchestrator.start_session(customer_id, channel="WHATSAPP")
    print(f"Session started: {session_id}")
    
    #user msg
    message = "I want to open an account"
    print(f"\nUser: {message}")
    event_bus.publish("USER_MESSAGE", {
        "session_id": session_id,
        "message": message
    })
    
    #state
    message = "My Aadhaar is 1234-5678-9012"
    print(f"\nUser: {message}")
    event_bus.publish("USER_MESSAGE", {
        "session_id": session_id,
        "message": message
    })

if __name__ == "__main__":
    main()
