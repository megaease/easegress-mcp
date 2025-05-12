from typing import Dict, List
from easegress_mcp.client import async_client
from easegress_mcp.log import logger
from easegress_mcp import schema
from urllib.error import HTTPError
import settings

urlPrefix = f"{settings.EG_API_ADDRESS}/apis/v1"


async def list_http_servers() -> list[schema.HTTPServer]:
    url = f"{urlPrefix}/objects"
    logger.info(f"Getting {url}")
    response = await async_client.get(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    result = [
        schema.HTTPServer(**item)
        for item in response.json()
        if item.get("kind") == "HTTPServer"
    ]
    return result


async def get_http_server(name: str) -> schema.HTTPServer:
    url = f"{urlPrefix}/objects/{name}"
    response = await async_client.get(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    result = schema.HTTPServer(**response.json())
    if result.kind != "HTTPServer":
        raise Exception(f"Object with name {name} is not an HTTPServer")

    return result


async def create_http_server(http_server: schema.HTTPServer):
    url = f"{urlPrefix}/objects"
    data = http_server.model_dump_json(exclude_none=True)
    logger.info(f"POST {url} with data: {data}")
    response = await async_client.post(url, data=data)

    if response.status_code != 201:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"HTTPServer {http_server.name} created successfully at {url}")


async def update_http_server(http_server: schema.HTTPServer):
    url = f"{urlPrefix}/objects/{http_server.name}"
    data = http_server.model_dump_json(exclude_none=True)

    print(f"update_http_server body: {data}")

    logger.info(f"PUT {url} with data: {data}")
    response = await async_client.put(url, data=data)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"HTTPServer updated successfully at {url}")


async def delete_http_server(name: str):
    url = f"{urlPrefix}/objects/{name}"
    logger.info(f"DELETE {url}")
    response = await async_client.delete(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"HTTPServer deleted successfully at {url}")


async def list_pipelines() -> list[schema.Pipeline]:
    url = f"{urlPrefix}/objects"
    logger.info(f"Getting {url}")
    response = await async_client.get(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    result = [
        schema.Pipeline(**item)
        for item in response.json()
        if item.get("kind") == "Pipeline"
    ]
    return result


async def get_pipeline(name: str) -> schema.Pipeline:
    url = f"{urlPrefix}/objects/{name}"
    logger.info(f"Getting {url}")

    response = await async_client.get(url)
    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    result = schema.Pipeline(**response.json())
    if result.kind != "Pipeline":
        raise Exception(f"Object with name {name} is not a Pipeline")

    return result


async def create_pipeline(pipeline: schema.Pipeline):
    url = f"{urlPrefix}/objects"
    data = pipeline.model_dump_json(exclude_none=True)

    print(f"create_pipeline body: {data}")

    logger.info(f"POST {url} with data: {data}")
    response = await async_client.post(url, data=data)

    if response.status_code != 201:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"Pipeline {pipeline.name} created successfully at {url}")


async def update_pipeline(pipeline: schema.Pipeline):
    url = f"{urlPrefix}/objects/{pipeline.name}"
    data = pipeline.model_dump_json(exclude_none=True)
    logger.info(f"PUT {url} with data: {data}")
    response = await async_client.put(url, data=data)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"Pipeline {pipeline.name} updated successfully at {url}")


async def delete_pipeline(name: str):
    url = f"{urlPrefix}/objects/{name}"
    logger.info(f"DELETE {url}")
    response = await async_client.delete(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"Pipeline {name} deleted successfully at {url}")


async def get_auto_cert_manager() -> schema.AutoCertManager:
    url = f"{urlPrefix}/objects/AutoCertManager"
    logger.info(f"Getting {url}")
    response = await async_client.get(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    result = schema.AutoCertManager(**response.json())
    if result.kind != "AutoCertManager":
        raise Exception("Object with name AutoCertManager is not an AutoCertManager")

    return result


async def create_auto_cert_manager(auto_cert_manager: schema.AutoCertManager):
    url = f"{urlPrefix}/objects"
    data = auto_cert_manager.model_dump_json(exclude_none=True)
    logger.info(f"POST {url} with data: {data}")
    response = await async_client.post(url, data=data)

    if response.status_code != 201:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(
        f"AutoCertManager {auto_cert_manager.name} created successfully at {url}"
    )


async def update_auto_cert_manager(auto_cert_manager: schema.AutoCertManager):
    url = f"{urlPrefix}/objects/AutoCertManager"
    data = auto_cert_manager.model_dump_json(exclude_none=True)
    logger.info(f"PUT {url} with data: {data}")
    response = await async_client.put(url, data=data)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(
        f"AutoCertManager {auto_cert_manager.name} updated successfully at {url}"
    )


async def delete_auto_cert_manager():
    url = f"{urlPrefix}/objects/AutoCertManager"
    logger.info(f"DELETE {url}")
    response = await async_client.delete(url)

    if response.status_code != 200:
        raise HTTPError(url, response.status_code, response.text, None, None)

    logger.info(f"AutoCertManager deleted successfully at {url}")
