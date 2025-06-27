import asyncio

from agents import Agent, Runner
from weather_agent import weather_agent

agent = Agent(
    name="Helpful agent",
    instructions="""You are a helpful agent. Be concise on your answers.
    
    IMPORTANT: Always provide a response with whatever information you have available. 
    If you cannot get complete information, provide a partial answer and explain what's missing.
    Do not keep trying indefinitely - give the best answer you can with the information available.""",
    handoffs=[weather_agent],
)


async def main():
    user_input = input("Enter your question: ")
    result = await Runner.run(agent, input=user_input)
    print(f"\nAgent response: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())