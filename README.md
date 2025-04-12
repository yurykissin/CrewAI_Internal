# 🧠 Adomatic CrewAI

This project is built on [CrewAI](https://docs.crewai.com), a framework for creating AI-native autonomous agent teams. The `Adomatic Crew` is a modular and configurable system designed to automate processes like creative generation, research, campaign planning, and more — using LLM-powered agents.

---

## 📁 Project Structure

```
├── src/
│   └── adomatic_crew/
│       ├── crew.py              # Entry point: defines and runs the crew
│       ├── main.py              # Main CLI for launching the crew
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   ├── tasks.yaml       # Task definitions
│       │   └── llms.py          # LLM configuration loader
│       ├── tools/
│       │   └── langsmith_loader.py  # Custom tools for agents
│       └── utils/
│           └── cache_utils.py   # Caching and state management
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── Dockerfile.dev               # Development Docker setup
├── SETUP.md                     # Full setup/configuration guide
└── README.md                    # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-org/crewai-adomatic.git
cd crewai-adomatic
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Edit the `.env` file to include your keys:

```ini
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
AGENTOPS_API_KEY=your_agentops_key
```
---

## 🚀 Running the Crew

To launch the AI crew:

```bash
python src/adomatic_crew/main.py
```

Make sure your `agents.yaml` and `tasks.yaml` are configured properly in `src/adomatic_crew/config/`.

---

## 🧠 Agent Configuration

You can modify your crew members and their capabilities in:

- `config/agents.yaml` — Roles, goals, personalities
- `config/tasks.yaml` — Task definitions and flow
- `config/llms.py` — Customize LLM models (e.g., OpenAI, Groq)

---

## 🛠 Custom Tools

You can create custom tools for your agents in:

- `src/adomatic_crew/tools/`

Example: `langsmith_loader.py` — Used to load LangSmith sessions as tools.

---

## 📦 Tech Stack

- [CrewAI](https://github.com/joaomdmoura/crewAI)
- LangChain
- Groq
- AgentOps
- Python 3.10+

---

## ✅ TODOs & Suggestions

- [ ] Add persistent memory or Redis support
- [ ] Include agent logs + error tracking
- [ ] Deploy to cloud for scheduled/automated runs
- [ ] Add web frontend for non-technical usage

---

🐳 VS Code Dev Container Setup

This project supports VS Code Dev Containers for a consistent development environment using Docker.

✅ Prerequisites
	•	VS Code
	•	Dev Containers Extension
	•	Docker

🚀 Quick Start
	1.	Open the project folder in VS Code.
	2.	When prompted, click “Reopen in Container”.
	3.	VS Code will build the image using Dockerfile.dev and open the containerized workspace.

Alternatively, open the Command Palette and run:
Dev Containers: Reopen in Container