import json
import subprocess
import sys
import time
import webbrowser
from datetime import datetime
from agents.severity_agent import SeverityAgent
from agents.priority_agent import PriorityAgent

# Step 1: Load test tickets from JSON file
with open("test_tickets.json", "r", encoding="utf-8") as f:
    test_tickets = json.load(f)

# Step 2: Routing logic
def route_ticket(severity_score, priority_score):
    if severity_score >= 8 and priority_score >= 8:
        return "Route to: VIP Escalation Team"
    elif severity_score >= 8:
        return "Route to: Critical Response Team"
    elif priority_score >= 8:
        return "Route to: Dedicated Customer Success Team"
    elif severity_score >= 5 or priority_score >= 5:
        return "Route to: Standard Support Team"
    else:
        return "Route to: Low Priority Queue"

# Step 3: Initialize agents
severity_agent = SeverityAgent()
priority_agent = PriorityAgent()

# Step 4: Analyze and collect results
all_results = []

for ticket in test_tickets:
    print(f"\n\n🧾 Processing {ticket['ticket_id']}")

    # Prepare input for agents
    severity_input = {
        "subject": ticket["subject"],
        "message": ticket["message"]
    }

    priority_input = {
        "customer_tier": ticket["customer_tier"],
        "monthly_revenue": ticket["monthly_revenue"],
        "previous_tickets": ticket["previous_tickets"],
        "account_age_days": ticket["account_age_days"]
    }

    # Run agents
    severity_output = severity_agent.agent.run(severity_input)
    priority_output = priority_agent.agent.run(priority_input)

    # Compute routing
    routing = route_ticket(severity_output.severity_score, priority_output.priority_score)

    # Log to ai_chat_history.txt with routing
    severity_agent.agent.run(severity_input, routing_decision=routing)
    priority_agent.agent.run(priority_input, routing_decision=routing)

    # Print summary to console
    print("Severity Agent Output:")
    print(severity_output)

    print("Priority Agent Output:")
    print(priority_output)

    print("Routing Decision:", routing)

    # Save result for dashboard
    ticket_result = {
        "ticket_id": ticket["ticket_id"],
        "severity_score": severity_output.severity_score,
        "severity_category": severity_output.severity_category,
        "priority_score": priority_output.priority_score,
        "priority_level": priority_output.priority_level,
        "routing_decision": routing,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    all_results.append(ticket_result)

# Step 5: Save all results to results.json
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print("\n All tickets processed and saved to results.json.")

# Step 6: Launch Streamlit Dashboard Automatically
time.sleep(2)  # (Optional) small delay to ensure filesystem is ready

try:
    print("\n Launching Streamlit dashboard...")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    
    # Open in default browser
    webbrowser.open("http://localhost:8501", new=2)
except Exception as e:
    print(" Could not auto-launch dashboard:", e)
    print("Run manually with: streamlit run dashboard.py")
