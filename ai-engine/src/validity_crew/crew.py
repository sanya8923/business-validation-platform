from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import yaml
from pathlib import Path


@CrewBase
class ValidityCrew():
    """ValidityCrew crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        # Load configurations
        config_path = Path(__file__).parent / 'config'
        
        with open(config_path / 'agents.yaml', 'r') as f:
            self.agents_config_data = yaml.safe_load(f)
        
        with open(config_path / 'tasks.yaml', 'r') as f:
            self.tasks_config_data = yaml.safe_load(f)
    
    @agent
    def requirements_analyst(self) -> Agent:
        config = self.agents_config_data['requirements_analyst']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def market_researcher(self) -> Agent:
        config = self.agents_config_data['market_researcher']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def competition_analyst(self) -> Agent:
        config = self.agents_config_data['competition_analyst']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def financial_projector(self) -> Agent:
        config = self.agents_config_data['financial_projector']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def risk_assessor(self) -> Agent:
        config = self.agents_config_data['risk_assessor']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def product_validator(self) -> Agent:
        config = self.agents_config_data['product_validator']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def operations_analyst(self) -> Agent:
        config = self.agents_config_data['operations_analyst']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def marketing_strategist(self) -> Agent:
        config = self.agents_config_data['marketing_strategist']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def technology_assessor(self) -> Agent:
        config = self.agents_config_data['technology_assessor']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def legal_advisor(self) -> Agent:
        config = self.agents_config_data['legal_advisor']
        return Agent(
            config=config,
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def report_generator(self) -> Agent:
        config = self.agents_config_data['report_generator']
        return Agent(
            config=config,
            verbose=True
        )
    
    @task
    def requirements_analysis_task(self) -> Task:
        config = self.tasks_config_data['requirements_analysis_task']
        return Task(
            config=config,
            agent=self.requirements_analyst()
        )
    
    @task
    def market_research_task(self) -> Task:
        config = self.tasks_config_data['market_research_task']
        return Task(
            config=config,
            agent=self.market_researcher()
        )
    
    @task
    def competition_analysis_task(self) -> Task:
        config = self.tasks_config_data['competition_analysis_task']
        return Task(
            config=config,
            agent=self.competition_analyst()
        )
    
    @task
    def financial_projection_task(self) -> Task:
        config = self.tasks_config_data['financial_projection_task']
        return Task(
            config=config,
            agent=self.financial_projector()
        )
    
    @task
    def risk_assessment_task(self) -> Task:
        config = self.tasks_config_data['risk_assessment_task']
        return Task(
            config=config,
            agent=self.risk_assessor()
        )
    
    @task
    def product_validation_task(self) -> Task:
        config = self.tasks_config_data['product_validation_task']
        return Task(
            config=config,
            agent=self.product_validator()
        )
    
    @task
    def operations_analysis_task(self) -> Task:
        config = self.tasks_config_data['operations_analysis_task']
        return Task(
            config=config,
            agent=self.operations_analyst()
        )
    
    @task
    def marketing_strategy_task(self) -> Task:
        config = self.tasks_config_data['marketing_strategy_task']
        return Task(
            config=config,
            agent=self.marketing_strategist()
        )
    
    @task
    def technology_assessment_task(self) -> Task:
        config = self.tasks_config_data['technology_assessment_task']
        return Task(
            config=config,
            agent=self.technology_assessor()
        )
    
    @task
    def legal_analysis_task(self) -> Task:
        config = self.tasks_config_data['legal_analysis_task']
        return Task(
            config=config,
            agent=self.legal_advisor()
        )
    
    @task
    def report_generation_task(self) -> Task:
        config = self.tasks_config_data['report_generation_task']
        return Task(
            config=config,
            agent=self.report_generator(),
            context=[
                self.requirements_analysis_task(),
                self.market_research_task(),
                self.competition_analysis_task(),
                self.financial_projection_task(),
                self.risk_assessment_task(),
                self.product_validation_task(),
                self.operations_analysis_task(),
                self.marketing_strategy_task(),
                self.technology_assessment_task(),
                self.legal_analysis_task()
            ]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the ValidityCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2
        )