from pydantic_ai_mock import OpenAIChatModel, PydanticAgent
from pydantic import BaseModel

class SeverityOutput(BaseModel):
    severity_score: int  # 1 to 10
    severity_category: str  # low, medium, high, critical
    reasoning: str

class SeverityAgent:
    def __init__(self):
        self.model = OpenAIChatModel(
            model="mistralai/mistral-7b-instruct:free", 
            api_key_env="OPENROUTER_API_KEY"
        )

        self.agent = PydanticAgent(
    model=self.model,
    system_prompt=(
        "You are a customer support severity analyzer. "
        "Given the subject and message of a ticket, evaluate how severe the issue is. "
        "Output a JSON object like this:\n"
        "{ \"severity_score\": <1-10>, \"severity_category\": \"low|medium|high|critical\", \"reasoning\": \"...\" }"
    ),
    output_model=SeverityOutput
)

    def analyze(self, subject: str, message: str) -> SeverityOutput:
        return self.agent.run({
            "subject": subject,
            "message": message
        })
