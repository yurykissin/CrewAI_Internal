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

# Together.ai LLaMA 
togetherai_llm = LLM(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    litellm_provider="together_ai"
)

# HuggingFace Phind/Phind-CodeLlama-34B-v2
hf_llm = LLM(
    model="huggingface/codellama/CodeLlama-13b-Instruct-hf",
    litellm_provider="huggingface"
)