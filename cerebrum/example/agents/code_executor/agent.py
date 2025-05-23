from cerebrum.tool.mcp_tool import MCPPool, MCPClient
from typing import List, Dict, Any
import asyncio
from cerebrum.llm.apis import llm_chat_with_tool_call_output

class CodeExecutor:
    def __init__(self):
        self.mcp_pool = MCPPool()
        self.description = "Execute shell commands, analyze code, and manage files seamlessly"
        
        
    async def initialize(self):
        code_executor_client = MCPClient.from_smithery(
            pkg_name="@auchenberg/claude-code-mcp",
            description="Execute shell commands, analyze code, and manage files seamlessly",
        )
        self.mcp_pool.add_mcp_client("code-executor", code_executor_client)
        await self.mcp_pool.start()
    
    def get_tool_information(self) -> List[Dict[str, Any]]:
        """Get all tool information for this worker"""
        return self.tool_information
    
    def get_tool_hints(self) -> str:
        """Get formatted tool hints for this worker"""
        hints = ""
        for tool_info in self.tool_information:
            hint = tool_info['hint']
            hints += f"- {hint}\n"
        return hints
    
    async def run(self, task_input: str) -> Dict[str, Any]:
        """Execute shell commands using the code-executor MCP"""
        # Implement shell command execution logic using code_executor_client
        # This is a placeholder - implement actual shell command execution here
        tool_information = await self.get_all_tool_information()
        tool_hints = self.get_tool_hints(tool_information)
        tool_schemas = self.get_all_tool_schemas(tool_information)
        
        tool_calls = llm_chat_with_tool_call_output(
            model="gpt-4o",
            messages=[{"content": task_input, "role": "user"}],
            tool_schemas=tool_schemas,
        )["response"]["tool_calls"]
        
        result = ""
        
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_result = await self.mcp_pool.clients[tool_name].execute(tool_args)
            result += tool_result
        
        return result
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.mcp_pool.stop()
