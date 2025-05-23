from dotenv import load_dotenv
import sys
load_dotenv()
from src.adomatic_crew.crew import AdomaticAgents
import os
from datetime import datetime
import time
import agentops
import litellm
import re

# Init liteLLM
#litellm.set_verbose = True
#litellm._turn_on_debug()

def remove_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Init agentops for 
agentops.init(os.getenv("AGENTOPS_API_KEY"))

# Create output directory
os.makedirs("reports", exist_ok=True)

# Generate a unique timestamp to differentiate log files per run
ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

print("Calling our crew of agents...")
# Redirect stdout and stderr to a log file
log_path = f"logs/session_log_{ts}.log"
sys.stdout = open(log_path, "w", encoding="utf-8")
sys.stderr = sys.stdout
print(f"Logging all output to {log_path}")

result = None
for _ in range(3):
    try:
        result = AdomaticAgents().crew().kickoff()
        break
    except litellm.RateLimitError as e:
        print("Rate limit hit. Retrying in 60s...")
        time.sleep(60)

if result:
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    print(f"Got result, exporting to full_report_{timestamp}.md")
else:
    print("❌ No result received after retries.")

# Reset stdout and stderr
sys.stdout.close()
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Auto-generate output file name
base_name, _ = os.path.splitext(log_path)
output_file = f"{base_name}.clean.txt"

# Read and clean
with open(log_path, 'r', encoding='utf-8') as f:
    raw_content = f.read()

clean_content = remove_ansi_sequences(raw_content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(clean_content)

print(f"✅ Full session log saved to {log_path}")