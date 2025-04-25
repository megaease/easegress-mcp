import asyncio
from enum import Enum
from typing import List

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server

from easegress_mcp import apis
from easegress_mcp import utils
from easegress_mcp import schema
from easegress_mcp import middleware
from easegress_mcp.log import logger


class EasegressTools(str, Enum):
    ListProxies = "list_proxies"
    CreateProxy = "create_proxy"
    DeleteProxy = "delete_proxy"
    UpdatePrxy = "update_proxy"
    GetProxy = "get_proxy"


async def change_middleware_state(arguments: dict, operation: int) -> List[TextContent]:
    arg = schema.MiddlewareNameSchema(**arguments)
    resp = await middleware.change_middleware_state(
        arg.middleware_instance_name, operation
    )
    return utils.to_textcontent(resp)


async def serve():
    server = Server("easegress")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=EasegressTools.ListProxies,
                description="List all proxies.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.CreateProxy,
                description="Create a proxy.",
                inputSchema=schema.MiddlewareNameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.DeleteProxy,
                description="Delete a proxy.",
                inputSchema=schema.MiddlewareNameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.UpdateProxy,
                description="Update a proxy.",
                inputSchema=schema.MiddlewareNameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.GetProxy,
                description="Get a proxy",
                inputSchema=schema.MiddlewareNameSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        logger.info(f"Call tool: {name}, arguments: {arguments}")
        match name:
            case EasegressTools.ListProxies:
                resp = await apis.list_Proxies()
                return utils.to_textcontent(resp)

            case EasegressTools.CreateProxy:
                resp = await apis.create_proxy()
                return utils.to_textcontent(resp)

            case EasegressTools.DeleteProxy:
                resp = await apis.delete_proxy()
                return utils.to_textcontent(resp)

            case EasegressTools.UpdatePrxy:
                resp = await apis.update_proxy()
                return utils.to_textcontent(resp)

            case _:
                raise ValueError(f"Unknown tool name: {name}")

    return server


def run():
    async def _run():
        server = await serve()
        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, options, raise_exceptions=True)

    asyncio.run(_run())
