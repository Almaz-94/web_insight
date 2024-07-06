import logging

import aiohttp

from config_data.configs import load_config

project_settings = load_config('.env')

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def do_get_request(session: aiohttp.ClientSession, url: str, params=None):
    if params is None:
        params = {}
    async with session.get(url, params=params) as response:
        response_data = await response.json()
        if response.status == 200:
            logger.info(" Запрос выполнен успешно")
        else:
            logger.info(f" An occurred error status code: {response.status}")
        return response_data


async def get_transcribed_text(text_id) -> str:
    host = project_settings.api_config.api_host_url
    api_endpoint = project_settings.api_config.get_transcribed_text
    url = host + api_endpoint
    params = {'id_text': text_id}

    async with aiohttp.ClientSession() as session:
        logger.info(" Получаем транскрибированный текст")
        res = await do_get_request(session=session, url=url, params=params)
        return res['text']


async def get_summary_text(text_id) -> str:
    host = project_settings.api_config.api_host_url
    api_endpoint = project_settings.api_config.get_summary_text
    url = host + api_endpoint
    params = {'id_text': text_id}

    async with aiohttp.ClientSession() as session:
        logger.info(" Получаем summary текст")
        res = await do_get_request(session=session, url=url, params=params)
        return res['summary_text']
