# 🧠 Customer Support Ticket Analyzer & Router

An AI-powered system that intelligently classifies and routes customer support tickets based on severity and priority using multi-agent architecture.

This project showcases how a real-world support workflow can be automated using prompt-based agents, structured outputs, and intelligent routing logic. It also includes a performance evaluation framework and a live Streamlit dashboard for insights.

---

## 🚀 Features

🔹 **Multi-Agent System**: Specialized AI agents for severity analysis and customer priority evaluation.
🔹 **Structured Reasoning**: Each agent provides scores (1–10) along with clear explanations.
🔹 **Routing Logic**: Smart rules route tickets to the right teams based on agent outputs.
🔹 **Evaluation Framework**: Validates routing decisions against expected outcomes.
🔹 **Auto Logging**: Logs each agent's input, output, and decision reasoning to `ai_chat_history.txt`.
🔹 **Dashboard**: Interactive Streamlit dashboard with filters, charts, KPIs, and trends over time.
🔹 **Scalable Input**: Supports dynamic ticket ingestion via `test_tickets.json`.

---

## 📁 Repository Structure
.
├── agents/
│ ├── severity_agent.py # Severity scoring agent
│ └── priority_agent.py # Priority scoring agent
│
├── assets/
│ └── architecture.png
│
├── test_tickets.json # Input sample tickets
├── results.json # Output final results
├── ai_chat_history.txt # AI reasoning logs
│
├── main.py # Core multi-agent execution
├── evaluation.py # Validate against expected outputs
├── dashboard.py # Streamlit visualization dashboard
├── pydantic_ai_mock.py # Core agent framework and logging
├── requirements.txt # Python project dependencies
├── .env # API key (not committed)

