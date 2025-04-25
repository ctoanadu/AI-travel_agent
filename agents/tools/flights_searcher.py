import os
from typing import Optional
import serpapi
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


class FlightsInput(BaseModel):
    departure_id: Optional[str] = Field(description='Departure airport code (IATA)')
    arrival_id: Optional[str] = Field(description='Arrival airport code (IATA)')
    outbound_date: Optional[str] = Field(description='Parameter defines the outbound date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    return_date: Optional[str] = Field(description='Parameter defines the return date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    adults: Optional[int] = Field(1, description='Parameter defines the number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Parameter defines the number of children. Default to 0.')
    infants_in_seat: Optional[int] = Field(0, description='Parameter defines the number of infants in seat. Default to 0.')
    infants_on_lap: Optional[int] = Field(0, description='Parameter defines the number of infants on lap. Default to 0.')
    type: Optional[int] = Field(1, description='Parameter defines the type of drip. Default to 2.')

@tool(args_schema=FlightsInput)
def flights_searcher(params: FlightsInput):
    '''
    Find flights using the Google Flights engine.

    Returns:
        dict: Flight search results.
    '''

    params = {
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
        search = serpapi.search(params)
        results = search.data.get("best_flights", "No flights found.")
        return results
    except Exception as e:
        print(f'error:{e}')
    
