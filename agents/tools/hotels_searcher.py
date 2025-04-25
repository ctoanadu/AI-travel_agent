import os
from typing import Any, Dict, Optional

import serpapi
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class HotelsInput(BaseModel):
    """
    Schema for input parameters required to search for hotels using SerpAPI.

    Attributes:
        q (str): Location for the hotel search.
        check_in_date (str): Check-in date in YYYY-MM-DD format.
        check_out_date (str): Check-out date in YYYY-MM-DD format.
        sort_by (Optional[str]): Sorting method. Default is by highest rating (value '8').
        adults (Optional[int]): Number of adults. Defaults to 1.
        children (Optional[int]): Number of children. Defaults to 0.
        rooms (Optional[int]): Number of rooms. Defaults to 1.
        hotel_class (Optional[str]): Comma-separated list of hotel star ratings to include (e.g., "3,4").
    """

    q: str = Field(description="Location of the hotel")
    check_in_date: str = Field(
        description="Check-in date. The format is YYYY-MM-DD. e.g. 2024-06-22"
    )
    check_out_date: str = Field(
        description="Check-out date. The format is YYYY-MM-DD. e.g. 2024-06-28"
    )
    sort_by: Optional[str] = Field(
        8,
        description="Parameter is used for sorting the results. Default is sort by highest rating",
    )
    adults: Optional[int] = Field(1, description="Number of adults. Default to 1.")
    children: Optional[int] = Field(0, description="Number of children. Default to 0.")
    rooms: Optional[int] = Field(1, description="Number of rooms. Default to 1.")
    hotel_class: Optional[str] = Field(
        None,
        description="Parameter defines to include only certain hotel class in the results. for example- 2,3,4",
    )


@tool(args_schema=HotelsInput)
def hotels_searcher(params: HotelsInput) -> Dict[str, Any]:
    """
    Searches for hotels using the Google Hotels engine through SerpAPI.

    Args:
        params (HotelsInput): Parameters for hotel search including location, dates, guests, and filters.

    Returns:
        dict: A dictionary containing up to five hotel listings based on the query parameters.

    Raises:
        Exception: If the search fails or returns no properties.
    """

    # Prepare query parameters
    search_params = {
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "engine": "google_hotels",
        "hl": "en",
        "gl": "us",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "currency": "USD",
        "adults": params.adults,
        "children": params.children,
        "rooms": params.rooms,
        "sort_by": params.sort_by,
        "hotel_class": params.hotel_class,
    }
    try:
        search = serpapi.search(search_params)
        results = search.data
        return results["properties"][:5]
    except Exception as e:
        print(f"Error occured during hotel search : {e}")
