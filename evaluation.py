import json
from main import route_ticket
from agents.severity_agent import SeverityAgent
from agents.priority_agent import PriorityAgent

# Load test tickets with expected field
with open("test_tickets.json", "r", encoding="utf-8") as f:
    test_tickets = json.load(f)

# Initialize agents
severity_agent = SeverityAgent()
priority_agent = PriorityAgent()

def evaluate(tickets):
    correct = 0
    for i, ticket in enumerate(tickets, 1):
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

        severity_output = severity_agent.agent.run(severity_input)
        priority_output = priority_agent.agent.run(priority_input)
        result = route_ticket(severity_output.severity_score, priority_output.priority_score)

        # Optional logging
        severity_agent.agent.run(severity_input, routing_decision=result)
        priority_agent.agent.run(priority_input, routing_decision=result)

        expected = ticket.get("expected", None)

        print(f"\nTest {i} – {ticket['ticket_id']}: {'✅' if result == expected else '❌'}")
        print(f"  Severity Score: {severity_output.severity_score}")
        print(f"  Priority Score: {priority_output.priority_score}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

        if result == expected:
            correct += 1

    print(f"\n Final Score: {correct} / {len(tickets)} correct")

if __name__ == "__main__":
    evaluate(test_tickets)
