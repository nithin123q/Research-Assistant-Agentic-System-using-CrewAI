import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	ScrapeWebsiteTool
)





@CrewBase
class ResearchAssistantAutomationCrew:
    """ResearchAssistantAutomation crew"""

    
    @agent
    def research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["research_specialist"],
            
            
            tools=[				SerperDevTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def content_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["content_analyst"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def research_report_writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["research_report_writer"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def find_research_sources(self) -> Task:
        return Task(
            config=self.tasks_config["find_research_sources"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_source_content(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_source_content"],
            markdown=False,
            
            
        )
    
    @task
    def create_research_report(self) -> Task:
        return Task(
            config=self.tasks_config["create_research_report"],
            markdown=True,
            
            guardrail="[ empty ]",
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ResearchAssistantAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
