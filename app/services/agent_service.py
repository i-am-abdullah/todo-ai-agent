from app.core.logging import get_logger
from app.utils.exceptions import AgentExecutionError
from app.agents.callbacks import TokenTrackingCallback
from app.core.config import get_settings

logger = get_logger(__name__)
settings = get_settings()


class AgentService:
    """Service for orchestrating AI agent interactions"""

    def __init__(self, agent_executor):
        self.agent_executor = agent_executor

    async def process_query(self, query: str) -> dict:
        """
        Process a natural language query through the AI agent
        
        Args:
            query: Natural language query from user
            
        Returns:
            dict with 'response', 'actions_taken', and 'usage'
        """
        try:
            logger.info(f"Processing agent query: {query}")
            
            # Create callback handler to track usage
            callback = TokenTrackingCallback(model_name=settings.OPENROUTER_MODEL)
            
            # Execute agent with the query and callback
            result = await self.agent_executor.ainvoke(
                {"input": query},
                config={"callbacks": [callback]}
            )
            
            # Extract response and actions
            response = result.get("output", "")
            actions_taken = self._extract_actions(result)
            usage_stats = callback.get_usage_stats()
            
            logger.info(f"Agent query completed. Actions: {actions_taken}, Tokens: {usage_stats.total_tokens}, Cost: ${usage_stats.estimated_cost_usd}")
            
            return {
                "response": response,
                "actions_taken": actions_taken,
                "usage": usage_stats,
            }
        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            raise AgentExecutionError(f"Failed to process query: {str(e)}")

    def _extract_actions(self, result: dict) -> list[str]:
        """Extract list of actions taken from agent result"""
        actions = []
        
        # Check intermediate steps for tool calls
        intermediate_steps = result.get("intermediate_steps", [])
        
        for i, step in enumerate(intermediate_steps, 1):
            try:
                # Each step is a tuple: (AgentAction, observation)
                if isinstance(step, tuple) and len(step) >= 2:
                    agent_action = step[0]
                    observation = step[1]
                    
                    # Extract tool name and input
                    if hasattr(agent_action, 'tool'):
                        tool_name = agent_action.tool
                        tool_input = agent_action.tool_input
                        
                        # Format the action nicely
                        if isinstance(tool_input, dict):
                            # Format dict inputs
                            input_str = ", ".join([f"{k}={v}" for k, v in tool_input.items() if v])
                            if input_str:
                                actions.append(f"{i}. {tool_name}({input_str})")
                            else:
                                actions.append(f"{i}. {tool_name}()")
                        else:
                            actions.append(f"{i}. {tool_name}({tool_input})")
                    
                    # Log for debugging
                    logger.debug(f"Action {i}: {agent_action}")
                    
            except Exception as e:
                logger.warning(f"Failed to parse step {i}: {e}")
                continue
        
        return actions

