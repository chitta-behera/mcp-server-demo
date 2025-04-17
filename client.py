import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_aws import ChatBedrock
import os
import json


server_params = StdioServerParameters(
    command="python", 
    args=["server.py"]
)

def llm_client(message:str):
    """
    Send a message to the LLM and return the response.
    """
    # Initialize the OpenAI client
    model_kwargs = {
        "max_tokens": 4096,
        "temperature": 0.0,
        "top_k": 50,
        "top_p": 0.5,
        "stop_sequences": ["\n\nHuman"],
    }
    aws_region = "us-east-1"
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name=aws_region,
        model_kwargs=model_kwargs
    )

    response = llm.invoke(message)

    # Extract and return the response content
    return response.content


def get_prompt_to_identify_tool_and_arguments(query,tools):
    tools_description = "\n".join([f"- {tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools])
    return  ("You are a helpful assistant with access to these tools:\n\n"
                f"{tools_description}\n"
                "Choose the appropriate tool based on the user's question. \n"
                f"User's Question: {query}\n"                
                "If no tool is needed, reply directly.\n\n"
                "IMPORTANT: When you need to use a tool, you must ONLY respond with "                
                "the exact JSON object format below, nothing else:\n"
                "Keep the values in str "
                "{\n"
                '    "tool": "tool-name",\n'
                '    "arguments": {\n'
                '        "argument-name": "value"\n'
                "    }\n"
                "}\n\n")


async def run(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read,write) as session:

            await session.initialize()

            # Get the list of available tools
            tools = await session.list_tools()

            prompt = get_prompt_to_identify_tool_and_arguments(query,tools.tools)
            llm_response = llm_client(prompt)

            tool_call = json.loads(llm_response)

            result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
            
            # Extract the text value from the result
            text_value = result.content[0].text

            return text_value


if __name__ == "__main__":
    query = "What is the output of 5+3"
    result = asyncio.run(run(query))
    print(result)