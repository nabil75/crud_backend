from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun



class SearchWebToolInput(BaseModel):
    """Input schema for SearchWebTool."""
    query: str = Field(
        ...,
        description="The search query to be executed through DuckDuckGo."
    )

class SearchWebTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Searches the web using DuckDuckGo and returns the top result for a given query."
    args_schema: Type[BaseModel] = SearchWebToolInput
    search_engine: DuckDuckGoSearchRun = Field(default_factory=DuckDuckGoSearchRun)
    
    def _run(self, query: str) -> str:
        """Execute the web search and return the top result.
        
        Args:
            query (str): The search query to be executed
            
        Returns:
            str: The search result from DuckDuckGo
        """
        try:
            result = self.search_engine.run(query, verbose=True, start_color="yellow")
            return result if result else "No results found for the given query."
            
        except Exception as e:
            return f"An error occurred while searching: {str(e)}"