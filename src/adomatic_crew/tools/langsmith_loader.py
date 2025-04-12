from langsmith import Client
import os
from dotenv import load_dotenv

load_dotenv()

def load_full_langsmith_research() -> str:
    print("[langsmith_loader] Loading reports from LangSmith")
    """Loads all documents from a LangSmith dataset and returns the joined content."""
    dataset_name = os.getenv("LANGSMITH_Dataset")
    api_key = os.getenv("LANGCHAIN_API_KEY")

    client = Client(api_key=api_key)

    #print("List of all datasets:")
    #for ds in client.list_datasets():
    #    print(ds.name)


    dataset = client.read_dataset(dataset_name=dataset_name)
    docs = client.list_examples(dataset_id=dataset.id)
    all_inputs = [d.inputs["input"] for d in docs]

    return "\n\n".join(all_inputs)