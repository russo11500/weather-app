import traceback
from datetime import datetime

import aiohttp
import aiohttp.client_exceptions
from fastapi import APIRouter, HTTPException

from src.config import Config as config
from src.logger import logger
from src.storage import Storage
from src.db import DB

router = APIRouter()


@router.get("/weather")
async def root(city: str):
    try:
        url = config.WEATHER_API_URL + config.WEATHER_API_ENDPOINT
        params = {
            'key': config.WEATHER_API_KEY,
            'q': city
        }
        storage = Storage(config.STORAGE_TYPE)
        if cashe := await storage.get_file(city):
            logger.info('Found cached file, skipping call to weather API')
            return cashe
        
        async with aiohttp.ClientSession() as session:
            logger.info('Cache file is missing, requestin weather API')
            async with session.get(url, params=params) as resp:
                resp.raise_for_status()
                logger.info('Got response from weather API')
                response = await resp.json()
            
        timestamp = datetime.now().timestamp()
        file_name = f'{city}_{timestamp}'
        logger.info(f'Uploading cache file {file_name} to storage {config.STORAGE_TYPE}')
        file_url = await storage.upload(file_name, response)
        if file_url:
            logger.info(f'Saving event to DB {config.DB_TYPE}')
            db = DB(config.DB_TYPE)
            await db.save_data(city, timestamp, file_url)

    except aiohttp.client_exceptions.ClientResponseError:
        logger.error(f'ERROR!!!\n {traceback.format_exc()}')
        raise HTTPException(status_code=400, detail='Failed to get weather data for provided city')
    except Exception:
        logger.error(f'ERROR!!!\n {traceback.format_exc()}')
        raise HTTPException(status_code=500, detail='Failed to get weather data')

    return response
