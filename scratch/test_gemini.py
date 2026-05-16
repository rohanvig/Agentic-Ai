import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, trace
from search_agent import search_agent
from planner_agent import planner_agent

load_dotenv(override=True)

async def test_agents():
    message = "Latest AI news in May 2026"
    
    print("Testing PlannerAgent with Gemini...")
    try:
        result = await Runner.run(planner_agent, message)
        print("PlannerAgent Success!")
        print(f"Searches: {result.final_output.searches}")
        
        if result.final_output.searches:
            first_query = result.final_output.searches[0]
            print(f"\nTesting SearchAgent with Gemini and DuckDuckGo for: {first_query.query}...")
            search_input = f"Search term: {first_query.query}\nReason: {first_query.reason}"
            search_result = await Runner.run(search_agent, search_input)
            print("SearchAgent Success!")
            print(f"Result snippet: {str(search_result.final_output)[:200]}...")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agents())
