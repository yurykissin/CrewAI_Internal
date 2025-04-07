from crewai import Crew, Process, Agent, Task, LLM
from crewai.project import CrewBase, agent, crew, task

llm=LLM(
	model="groq/meta-llama/llama-4-scout-17b-16e-instruct"
)

@CrewBase
class AdomaticAgents():
	@agent
	def tech_architect(self):
		return Agent(
			config=self.agents_config['tech_architect'],
    	verbose=True,
		llm=llm
		)
      
	@agent
	def ui_ux_designer(self):
		return Agent(
			config=self.agents_config['ui_ux_designer'],
    	verbose=True,
		llm=llm
		)

	@agent
	def frontend_dev(self):
		return Agent(
            config=self.agents_config['frontend_dev'],
        verbose=True,
        llm=llm
        )
	@agent
	def backend_dev(self):
		return Agent(
            config=self.agents_config['backend_dev'],
            verbose=True,
            llm=llm
        )
	@agent
	def prompt_engineer(self):
		return Agent(
            config=self.agents_config['prompt_engineer'],
            verbose=True,
            llm=llm
        )
	@agent
	def product_manager(self):
		return Agent(
            config=self.agents_config['product_manager'],
        verbose=True,
        llm=llm 
    )
	@agent
	def qa_agent(self):  
		return Agent(
            config=self.agents_config['qa_agent'],
        verbose=True,
        llm=llm
        )
	
	@task
	def tech_architecture(self):
		return Task(
			config=self.tasks_config['tech_architecture'],
			verbose=True
		)

	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)