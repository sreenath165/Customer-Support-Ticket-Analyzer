from pydantic_ai_mock import OpenAIChatModel, PydanticAgent
from pydantic import BaseModel

class PriorityOutput(BaseModel):
    priority_score: int  # 1 to 10
    priority_level: str  # low, medium, high, vip
    reasoning: str

class PriorityAgent:
    def __init__(self):
        self.model = OpenAIChatModel(
            model="mistralai/mistral-7b-instruct:free",
            api_key_env="OPENROUTER_API_KEY"
        )

        self.agent = PydanticAgent(
            model=self.model,
            system_prompt=(
                "You are a priority classification assistant for customer support. "
                "Given customer details like tier, revenue, past tickets, and account age, "
                "determine how high-priority the support request should be.\n\n"
                "Output format:\n"
                "{ \"priority_score\": <1-10>, \"priority_level\": \"low|medium|high|vip\", \"reasoning\": \"...\" }"
            ),
            output_model=PriorityOutput
        )

    def analyze(self, ticket_data: dict) -> PriorityOutput:
        return self.agent.run({
            "customer_tier": ticket_data["customer_tier"],
            "monthly_revenue": ticket_data["monthly_revenue"],
            "previous_tickets": ticket_data["previous_tickets"],
            "account_age_days": ticket_data["account_age_days"]
        })
