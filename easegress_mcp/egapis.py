from typing import Dict
from easegress_mcp.client import async_client
from easegress_mcp.log import logger
from easegress_mcp import schema
import settings

urlPrefix = f"{settings.EG_API_ADDRESS}/apis/v1"


async def list_HTTPServers():
    url = f"{urlPrefix}/objects"
    logger.info(f"Getting {url}")
    response = await async_client.get(url)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    result = [item for item in response.json() if item.get("kind") == "HTTPServer"]
    return result


async def get_HTTPServer(arguments: Dict):
    name = arguments.get("name")
    if not name:
        raise ValueError("name is required")
    url = f"{urlPrefix}/objects/{name}"
    response = await async_client.get(url)
    if response.status_code != 200:
        raise Exception(f"GET {url} Error: {response.status_code} - {response.text}")

    result = response.json()
    if result.get("kind") != "HTTPServer":
        raise Exception(f"Object with name {name} is not an HTTPServer")

    return result


async def create_HTTPServer(arguments: Dict):
    try:
        http_server = schema.HTTPServerSchema(**arguments)
        url = f"{urlPrefix}/objects"
        data = http_server.model_dump_json(exclude_none=True)
        logger.info(f"POST {url} with data: {data}")
        response = await async_client.post(url, data=data)

        if response.status_code == 201:
            logger.info(f"HTTPServer created successfully at {url}")
            return "succeed"

        raise Exception(f"POST {url} Error: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"create HTTPServer {url} {data}: {e}")


async def update_HTTPServer(arguments: Dict):
    name = arguments.get("name")
    if not name:
        raise ValueError("name is required")
    url = f"{urlPrefix}/objects/{name}"
    try:
        http_server = schema.HTTPServerSchema(**arguments)
        data = http_server.model_dump_json(exclude_none=True)
        logger.info(f"PUT {url} with data: {data}")
        response = await async_client.put(url, data=data)

        if response.status_code == 200:
            logger.info(f"HTTPServer updated successfully at {url}")
            return "succeed"

        raise Exception(f"PUT {url} Error: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"update HTTPServer {url} {data}: {e}")


async def delete_HTTPServer(arguments: Dict):
    name = arguments.get("name")
    if not name:
        raise ValueError("name is required")
    url = f"{urlPrefix}/objects/{name}"
    logger.info(f"DELETE {url}")
    response = await async_client.delete(url)

    if response.status_code == 200:
        logger.info(f"HTTPServer deleted successfully at {url}")
        return "succeed"

    raise Exception(f"DELETE {url} Error: {response.status_code} - {response.text}")


async def list_ProxyPipelines():
    pass


async def get_ProxyPipeline(arguments: Dict):
    pass


async def create_ProxyPipeline(arguments: Dict):
    pass


async def update_ProxyPipeline(aryguments: Dict):
    pass


async def delete_ProxyPipeline(arguments: Dict):
    pass
