from agents import Agent
from weather_tools import get_coordinates, get_weather, get_days_between_dates, get_today

weather_agent = Agent(
    name="Weather agent",
    instructions="""Provide the weather forecast for up to seven days ahead.
    
    IMPORTANT: If any tool fails or returns an error, provide whatever information you can gather and explain what went wrong. 
    Do not retry tools multiple times - if a tool fails once, move on and provide the best answer possible with available data.
    Always return a response, even if partial.""",
    tools=[get_coordinates, get_weather, get_days_between_dates, get_today],
)