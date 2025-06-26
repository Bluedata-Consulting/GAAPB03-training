
from mcp.server.fastmcp import FastMCP
import wikipedia
import requests, json

mcp = FastMCP("myMCP")

@mcp.tool()
async def get_current_weather(city:str)->dict:
    """ can be used to get/fetch current weather information for a city name
    """
    api_key = "6a8b0ac166a37e2b7a38e64416b3c3fe"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    response = response.content.decode()
    response = json.loads(response)
    output = {"City Name":city,"weather":response["weather"][0]['description'],
              "temperature":response['main']['temp'],
              "unit":"kelvin"}

    return output


@mcp.tool()
async def get_wikipedia_pages(query:str)->list:
    info = wikipedia.search(query)
    return info


if __name__=="__main__":
    mcp.run(transport="http")

