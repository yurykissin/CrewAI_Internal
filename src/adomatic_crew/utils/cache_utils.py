import os
import json

def get_cached_agent_output(agent_role: str) -> dict | None:
    file_path = os.path.join(os.path.dirname(__file__), "..", "cache", "agent_outputs", f"{agent_role.replace(' ', '_').lower()}.json")
    file_path = os.path.abspath(file_path)
    print(f"[CACHE_UTILS] Looking if a previous run has an output in: {file_path}")
    if os.path.exists(file_path):
        print("[CACHE_UTILS] Found a previous output, using it...")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f).get("output")
            #print(f"[CACHE_UTILS] output is:\n", {output})
            return data
    return None

def save_agent_output(agent_role: str, output: str):
    file_path = os.path.join(os.path.dirname(__file__), "..", "cache", "agent_outputs", f"{agent_role.replace(' ', '_').lower()}.json")
    file_path = os.path.abspath(file_path)
    print(f"[CACHE_UTILS] Saving new output to: ", {file_path})
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"output": output}, f, ensure_ascii=False, indent=2)