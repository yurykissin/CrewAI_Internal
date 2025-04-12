from crewai import Crew, Process, Agent, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.task_output import TaskOutput
from src.adomatic_crew.config.llms import groq_llm, fireworks_llm
from src.adomatic_crew.tools.langsmith_loader import load_full_langsmith_research
from utils.cache_utils import get_cached_agent_output, save_agent_output
import time
import os

@CrewBase
class AdomaticAgents():
	def __init__(self):
		print("Initializing AdomaticAgents and mapping agent variables...")
		self.llm_throttle_seconds = 60

	print("Loading YAML confiugration files ")
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def task_callback(self, task_result, **kwargs):
		# Determine agent role
		agent_role = getattr(task_result, "agent", "unknown")

		output_text = task_result.raw

		# Save structured cache
		save_agent_output(
			task_result.name,
			{
				"description": task_result.description,
				"expected_output": task_result.expected_output,
				"output": {
					"description": task_result.description,
					"agent": agent_role,
					"output": output_text
				}
			}
		)
		print(f"[✅ CALLBACK] Output saved for task: {task_result.name}")

		try:
			os.makedirs("/code/reports", exist_ok=True)
			timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

			# ✅ Append to cumulative full report
			full_md_path = f"/code/reports/full_output_latest_{timestamp}.md"
			with open(full_md_path, "a") as full_report:
				full_report.write(f"\n\n---\n\n# Task: {task_result.name}\n\n")
				full_report.write(f"**Agent**: {agent_role}\n\n")
				full_report.write(f"**Description**:\n{task_result.description}\n\n")
				full_report.write(f"**Expected Output**:\n{task_result.expected_output}\n\n")
				full_report.write(f"**Result**:\n\n{output_text}\n")
			
			print(f"[✅ CALLBACK] Markdown report saved to {full_md_path}")


		except Exception as e:
			print(f"[❌ CALLBACK ERROR] Could not save markdown report: {e}")

	# Defining the Project manager agent. This agent will receive the output from the PM and break it into tasks, sprints and etc...
	@agent
	def project_manager(self) -> Agent:
		config=self.agents_config['project_manager']
		return Agent(
			config=config,
			name=config["role"],
			llm=fireworks_llm.model
		)
	
	# Defining the Product manager agent. This is the main agent who receives as input link to langsmith dataset. The output of this agent is MVP strategy
	@agent
	def product_manager(self) -> Agent:
		config=self.agents_config['product_manager']
		return Agent(
			config=config,
			name=config["role"],
			llm=fireworks_llm.model
		)

	@agent
	def technical_architect(self) -> Agent:
		config=self.agents_config['technical_architect']
		return Agent(
			config=config,
			name=config["role"],
			llm=fireworks_llm.model
		)
      
	@agent
	def ux_designer(self) -> Agent:
		config=self.agents_config['ux_designer']
		return Agent(
			config=config,
			name=config["role"],
			llm=fireworks_llm.model
		)
	
	@agent
	def market_researcher(self) -> Agent:
		config=self.agents_config['market_researcher']
		return Agent(
			config=config,
			name=config["role"],
			llm=fireworks_llm.model
		)
	
	@task
	def initiate_market_research(self) -> Task:
		task = Task(
			config=self.tasks_config["initiate_market_research"],
			callback=self.task_callback,
			verbose=True
		)
		return task
	
	@task
	def create_execution_plan(self) -> Task:
		task = Task(
			config=self.tasks_config['create_execution_plan'],
			callback=self.task_callback,
			verbose=True
		)
		return task
	
	@task
	def define_mvp_strategy(self) -> Task:
		research = load_full_langsmith_research()
		task = Task(
			config=self.tasks_config['define_mvp_strategy'],
			verbose=True,
			instructions=f"""
				You are working from the following research. Use it to define the MVP, feature priorities, key risks, and any needed roles:

				--- START OF RESEARCH ---
				{research}
				--- END OF RESEARCH ---
			""",
			callback=self.task_callback
		)
		return task
	
	@task
	def design_user_interface(self) -> Task:
		task = Task(
			config=self.tasks_config['design_user_interface'],
			callback=self.task_callback,
			verbose=True
		)
		return task
	
	@task
	def define_architecture_plan(self) -> Task:
		task = Task(
			config=self.tasks_config['define_architecture_plan'],
			callback=self.task_callback,
			verbose=True
		)
		return task
	
	@task
	def market_research_analysis(self) -> Task:
		task = Task(
			config=self.tasks_config['market_research_analysis'],
			callback=self.task_callback,
			verbose=True
		)
		return task

	@crew
	def crew(self) -> Crew:
		print("Creating crew with hierarchical orchestration...")

		manager_key = "project_manager"
		# 👇 This maps readable names (used by coworker tools) to the actual agent instances
		agent_dict = {
			"Market Research Analyst": self.market_researcher(),
			"Product Manager Agent": self.product_manager(),
			"Technical Architect Agent": self.technical_architect(),
			"UX Designer": self.ux_designer(),
		}

		crew_instance = Crew(
			agents=list(agent_dict.values()),
			tasks=[
				self.initiate_market_research(),
				self.market_research_analysis(),
				self.define_mvp_strategy(),
				self.create_execution_plan(),
				self.define_architecture_plan(),
				self.design_user_interface(),
			],
			manager_agent=self.project_manager(),  # Lead agent
			process=Process.hierarchical,
			verbose=True,
			task_callback=self.task_callback
		)
		print("[DEBUG] Agents in crew:")
		for a in crew_instance.agents:
			print(f" - {type(a)}")
			print(f" - full object: {a}")

		print("[DEBUG] Registered coworkers:")
		for agent in crew_instance.agents:
			print(f" - {agent.agent_ops_agent_name}")

		return crew_instance