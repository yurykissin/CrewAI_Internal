# llms.py
from crewai import LLM

# Groq LLaMA 4 Scout
groq_llm = LLM(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct"
)

# Fireworks LLaMA 2 Chat 13B
fireworks_llm = LLM(
    #model="fireworks/llama-v2-13b-chat",
    model="fireworks_ai/accounts/fireworks/models/llama-v3p1-8b-instruct", 
    #model="fireworks/llama-v3p1-8b-instruct",
    litellm_provider="fireworks"
)