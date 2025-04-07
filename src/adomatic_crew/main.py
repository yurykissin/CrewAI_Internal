from dotenv import load_dotenv
load_dotenv()
from src.adomatic_crew.crew import AdomaticAgents
import os
import agentops

agentops.init(os.getenv("AGENTOPS_API_KEY"))

print("Calling our crew of agents...")
result = AdomaticAgents().crew().kickoff()
print(result)

