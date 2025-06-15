from typing import List, Optional
from smolagents import CodeAgent, LiteLLMModel, tool

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(
        self,
        name: str,
        description: str,
        tools: List[tool],
        model_id: str = "anthropic/claude-3-5-sonnet-latest",
        temperature: float = 0.5
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent's purpose
            tools: List of tools available to the agent
            model_id: ID of the model to use
            temperature: Temperature setting for the model
        """
        self.agent = CodeAgent(
            tools=tools,
            model=LiteLLMModel(
                model_id=model_id,
                temperature=temperature
            ),
            name=name,
            description=description
        )
    
    def run(self, task: str) -> str:
        """
        Run the agent with a given task.
        
        Args:
            task: The task to execute
            
        Returns:
            str: The result of the task execution
        """
        return self.agent.run(task) 