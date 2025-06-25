# Customer Support Ticket Analyzer & Router

An AI-powered system that intelligently classifies and routes customer support tickets based on severity and priority using multi-agent architecture.

This project showcases how a real-world support workflow can be automated using prompt-based agents, structured outputs, and intelligent routing logic. It also includes a performance evaluation framework and a live Streamlit dashboard for insights.

---

## 🚀 Features

- **Multi-Agent System**: Specialized AI agents for severity analysis and customer priority evaluation.
- **Structured Reasoning**: Each agent provides scores (1–10) along with clear explanations.
- **Routing Logic**: Smart rules route tickets to the right teams based on agent outputs.
- **Evaluation Framework**: Validates routing decisions against expected outcomes.
- **Auto Logging**: Logs each agent's input, output, and decision reasoning to `ai_chat_history.txt`.
- **Dashboard**: Interactive Streamlit dashboard with filters, charts, KPIs, and trends over time.
- **Scalable Input**: Supports dynamic ticket ingestion via `test_tickets.json`.

---

## ⚙️ Setup Instructions

1. Clone the repo and install the required dependencies:

```bash
git clone https://github.com/sreenath165/Customer-Support-Ticket-Analyzer-And-Router.git
cd Customer-Support-Ticket-Analyzer-And-Router

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

streamlit dashboard.py            # If the dashboard doesn't open automatically
```

## 📦 Folder Structure

```plaintext
.
├── agents/
│   ├── severity_agent.py
│   └── priority_agent.py
├── test_tickets.json         # ✅ Input tickets
├── results.json              # ✅ Output results
├── main.py                   # 🔁 Main entry point
├── evaluation.py             # ✅ Evaluation of model routing
├── streamlit_dashboard.py    # 📊 Dashboard UI
├── ai_chat_history.txt       # 📄 Full chat logs
├── pydantic_ai_mock.py       # 🧠 Pydantic-style mock
├── .env                      # 🔐 Your API key goes here
├── requirements.txt
```

## 💡 NOTE: 
- You must use your own API key. This project does not come with any pre-set API keys.
- You can use any LLM provider supported by OpenRouter, such as:
          mistralai/mistral-7b-instruct
          openai/gpt-3.5-turbo
          meta-llama/llama-3-8b-instruct etc.
- Ensure that you update the API Key environment variable and the LLM model in agents/severity_agent.py and agents/priority_agent.py and update the pydantic_ai_mock.py
- This allows you to plug in different models of your choice as long as they follow the respective-compatible chat APIs.

## 🔁 Step-by-Step Process
The system uses multi-agent prompt-based AI to classify and route support tickets automatically.

🗃️ Ticket Input
test_tickets.json contains all incoming support tickets in JSON format.

📤 Agent Processing
Each ticket is sent to:
SeverityAgent → analyzes the subject + message
PriorityAgent → evaluates customer metadata (tier, revenue, etc.)

🧠 Model Reasoning
Each agent generates:
A score (1–10)
A category/label (like "critical", "low")
A clear explanation for its decision

🚦 Routing Logic
The results are passed to the route_ticket() function in main.py, which decides:
If it should go to VIP support, critical response or low-priority queue

📝 Logging
All agent inputs/outputs and reasoning are logged to ai_chat_history.txt with timestamps.

📄 Results Saving
Outputs are saved in results.json which is later used by Streamlit dashboard for visualization.

📊 Dashboard
You can view everything interactively via streamlit_dashboard.py.

## 💼 Use Cases & Benefits
This system can be adapted to many real-world scenarios:
| Use Case                           | How It Helps                                                      |
| ---------------------------------  | ----------------------------------------------------------------- |
| ✅ **Customer Support Automation** | Classify, prioritize, and route support tickets instantly         |
| ✅ **Product Feedback Analysis**   | Spot critical bugs vs minor UI issues                             |
| ✅ **SaaS Tier-Based Support**     | Prioritize enterprise/premium customers dynamically               |
| ✅ **AI Model Evaluation**         | Plug in new LLMs and test their reasoning and routing consistency |
| ✅ **Agent Research**              | Extend to more agents (e.g., sentiment, complexity, urgency)      |
