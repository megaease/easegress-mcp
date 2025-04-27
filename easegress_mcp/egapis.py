from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

from easegress_mcp.client import async_client
from easegress_mcp.log import logger
import settings


class HTTPServer(BaseModel):
    pass


class ProxyPipeline(BaseModel):
    pass


async def list_HTTPServers():
    url = f"{settings.EG_API_ADDRESS}/apis/v1/objects"
    response = await async_client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


async def get_HTTPServer(name: str):
    pass


async def create_HTTPServer(http_server: HTTPServer):
    pass


async def update_HTTPServer(name: str, http_server: HTTPServer):
    pass


async def delete_HTTPServer(name: str):
    pass


async def list_ProxyPipelines():
    pass


async def get_ProxyPipeline(name: str):
    pass


async def create_ProxyPipeline(proxy_pipeline: ProxyPipeline):
    pass


async def update_ProxyPipeline(name: str, proxy_pipeline: ProxyPipeline):
    pass


async def delete_ProxyPipeline(name: str):
    pass
