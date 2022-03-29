"""Module for converting currencies using FastAPI"""

import os
from datetime import date

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import httpx
from dotenv import load_dotenv


# Initialize python-dotenv to load environment variables
load_dotenv()

# Initialize environment variables
BASE_API_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_SECRET_KEY')
LATEST_CURRENCY_PATH = 'latest?apikey='
CONVERT_CURRENCY_PATH ='convert?api='


# Create instance of FastAPI as app
app = FastAPI()


# Initialize router instance for homepage and documentation
router = APIRouter(
    tags=['Homepage and Documentation Endpoints']
)

# Initialize router instance for conversion endpoints
converter_router = APIRouter(
    prefix='/api/converter/v1', tags=['FastAPI Currency Conversion Endpoints']
)


# Initialize templating engine.
# Look for template files in templates sub-directory of project folder
templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)  # Return response as HTML page
def home(request: Request):
    """Return HTML page response with links to other API endpoints."""
    return templates.TemplateResponse(
        'home.html', # Use home.html template in templates directory
        {
            'request': request, 'context': {
                'swagger_docs': '/docs/', 'open_api_docs': '/redoc/',
                'supported_currencies': '/api/converter/v1'
            }
        }
    )


# Start declaring the conversion endpoints here
@converter_router.get('/')
async def get_supported_currency():
    """Returns all the supported currencies and exchange rate

    Looks up the currenct exchange rates and returns the conversion rates based
    on the given Base Currency (Default=USD).
    """
    # Initialize remote api URL
    supported_currency_url = BASE_API_URL + LATEST_CURRENCY_PATH + API_KEY

    # Make request of latest rates from API provider using httpx library
    async with httpx.AsyncClient() as client:
        response = await client.get(supported_currency_url)
        json_response = response.json() # Convert response
        # Loop through the result and extract each rate with corresponding value.
        rates = dict() # Initialize empty rates dictionary
        for currency_rate in json_response['data'].items():
            rates.update({currency_rate[1]['code']: currency_rate[1]['value']})

        return {'supported_currency_rates': rates}


# Convert api endpoint
@converter_router.get('/convert')
async def convert_currency(
    amount: float, base_currency: str = "USD", target_currency: str = ""
):
    """Converts given amount from one currency to another.

    Args:
        amount (float): The amount to be converted.
        base_currency (str, optional): The currency from which conversion is
        done.
        target_currency (str, optional): The currency which amount is
        converted to.
    Description:
        Takes amount and converts it to the given target currency using rate of
        base currency. If base_currency is not provided, it defaults to USD.
        If target_currency is not provided, it defaults to all availbale
        currencies.
    """

    # Do basic checks and then construct the appropriate URL.
    if not amount:
        return {'error': 'Amount is a required field.'}

    path_parameters = f'&value={amount}&base_currency={base_currency}' \
        f'&currencies={target_currency}'
    # Initialize remote conversion api URL.
    converter_url = f'{BASE_API_URL}{CONVERT_CURRENCY_PATH}{API_KEY}' \
        f'{path_parameters}'

    # Request the remote api to do the conversion.
    async with httpx.AsyncClient() as client:
        response = await client.get(converter_url)
        json_response = response.json() # Convert response
        # Loop through the response and extract each conversion.
        conversion = dict() # Initialize empty conversion dictionary
        for currency_rate in json_response['data'].items():
            conversion.update(
                {currency_rate[1]['code']: currency_rate[1]['value']}
            )

        return {'conversion_rate': conversion}


# Historical rates API endpoint
@converter_router.get('/historical-data')
async def get_historical_data(
    rates_date: date, base_currency: str = "USD", target_currency: str = ''
):
    """Returns historical conversion rates based on rates_date.

    Args:
        rates_date (date): Date to retrieve historical rates from
        (format: 2022-03-29).
        base_currency (str, optional): The base currency to return conversion.
        Defaults to "USD".
        target_currency (str, optional): The targetted currency which
        conversion will be in. Defaults to "" string. If no value is given,
        conversion will be done for all currencies.
    """
    if not rates_date:
        return {'error': 'rates_date is a required field.'}

    path_parameters = f'&date={rates_date}&base_currency={base_currency}' \
        f'&currencies={target_currency}'
    history_rates_url = BASE_API_URL+'historical?api='+API_KEY+path_parameters

    # Request the remote api to get historical data.
    async with httpx.AsyncClient() as client:
        response = await client.get(history_rates_url)
        json_response = response.json() # Convert response
        # Loop through the response and extract each history rate.
        historical_rate = dict() # Initialize empty historical rate dictionary
        for history_rate in json_response['data'].items():
            historical_rate.update(
                {history_rate[1]['code']: history_rate[1]['value']}
            )

        return {'historical_rate': historical_rate}


# Initialize home page URL.
app.include_router(router)
app.include_router(converter_router)


# Run this converter when invoked as the main file.
if __name__ == "__main__":
    uvicorn.run("converter:app", host="127.0.0.1", port=8700)
