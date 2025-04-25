from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

from easegress_mcp.client import async_client
from easegress_mcp.log import logger


class HTTPServer(BaseModel):
    pass


class FilterProxy(BaseModel):
    pass


async def list_proxies():
    pass


async def create_proxy():
    pass


async def delete_proxy():
    pass


async def update_proxy():
    pass


async def get_proxy():
    pass
