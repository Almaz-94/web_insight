import logging

import aiohttp

from config_data.configs import load_config

settings = load_config('.env')

logging.basicConfig(level=logging.INFO)


async def do_get_request(session: aiohttp.ClientSession, url: str, params=None):
    if params is None:
        params = {}
    async with session.get(url, params=params) as response:
        logging.info(f"Requested URL: {url} with params: {params}")
        response_data = await response.json()
        logging.info(f"Response data: {response_data}")
        return response_data


async def get_transcribed_text(text_id) -> str:
    host = settings.api_config.api_host_url
    api_endpoint = settings.api_config.get_transcribed_text
    url = host + api_endpoint
    params = {'id_text': text_id}

    logging.info(f"Fetching transcribed text with text_id: {text_id}")

    async with aiohttp.ClientSession() as session:
        res = await do_get_request(session=session, url=url, params=params)
        return res['text']


async def get_summary_text(text_id) -> str:
    host = settings.api_config.api_host_url
    api_endpoint = settings.api_config.get_summary_text
    url = host + api_endpoint
    params = {'id_text': text_id}

    async with aiohttp.ClientSession() as session:
        res = await do_get_request(session=session, url=url, params=params)
        return res['summary_text']
