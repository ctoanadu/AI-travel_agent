import os
from typing import Optional, Dict, Any
import serpapi
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from dotenv import load_dotenv

#Load environment virables form .env file 
load_dotenv()


class FlightsInput(BaseModel):
    """
    Schema for input parameters for flight search.

    Attributes:
        departure_id (Optional[str]): The IATA code for the departure airport.
        arrival_id (Optional[str]): The IATA code for the arrival airport.
        outbound_date (Optional[str]): The outbound flight date in YYYY-MM-DD format.
        return_date (Optional[str]): The return flight date in YYYY-MM-DD format.
        adults (Optional[int]): The number of adults for the flight search. Defaults to 1.
        children (Optional[int]): The number of children for the flight search. Defaults to 0.
        infants_in_seat (Optional[int]): The number of infants requiring a seat. Defaults to 0.
        infants_on_lap (Optional[int]): The number of infants traveling on a lap. Defaults to 0.
        types (Optional[int]): The type of flight search. Defaults to 1.
    """
    departure_id: Optional[str] = Field(description='Departure airport code (IATA)')
    arrival_id: Optional[str] = Field(description='Arrival airport code (IATA)')
    outbound_date: Optional[str] = Field(description='Parameter defines the outbound date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    return_date: Optional[str] = Field(description='Parameter defines the return date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    adults: Optional[int] = Field(1, description='Parameter defines the number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Parameter defines the number of children. Default to 0.')
    infants_in_seat: Optional[int] = Field(0, description='Parameter defines the number of infants in seat. Default to 0.')
    infants_on_lap: Optional[int] = Field(0, description='Parameter defines the number of infants on lap. Default to 0.')
    types: Optional[int] = Field(1, description='Parameter defines the type of drip. Default to 2.')

@tool(args_schema=FlightsInput)
def flights_searcher(params: FlightsInput) -> Dict[str, Any]:
    """
    Searches for flights using the Google Flights engine via SerpAPI.

    Args:
        params (FlightsInput): The input parameters for the flight search.

    Returns:
        dict: A dictionary containing flight search results. If no flights are found, returns a message.
    
    Raises:
        Exception: If an error occurs during the search process.
    """

    # Prepare the search parameters
    search_params = {
        'api_key': os.environ.get('SERPAPI_API_KEY'),
        'engine': 'google_flights',
        'hl': 'en',
        'gl': 'us',
        'departure_id': params.departure_id,
        'arrival_id': params.arrival_id,
        'outbound_date': params.outbound_date,
        'return_date': params.return_date,
        'currency': 'USD',
        'adults': params.adults,
        'infants_in_seat': params.infants_in_seat,
        'stops': '1',
        'infants_on_lap': params.infants_on_lap,
        'children': params.children,
        'type':params.type
    }

    try:
        search = serpapi.search(search_params)
        results = search.data.get("best_flights", "No flights found.")
        return results
    except Exception as e:
        print(f'error:{e}')
    
