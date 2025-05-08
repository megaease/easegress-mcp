import asyncio
from enum import Enum
from typing import List

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server

from easegress_mcp import tools
from easegress_mcp import utils
from easegress_mcp import schema
from easegress_mcp.log import logger


class EasegressTools(str, Enum):
    ListHTTPReverseProxies = "ListHTTPReverseProxies"
    CreateHTTPReverseProxy = "CreateHTTPReverseProxy"
    DeleteHTTPReverseProxy = "DeleteHTTPReverseProxy"
    UpdateHTTPReverseProxy = "UpdateHTTPReverseProxy"
    GetHTTPReverseProxy = "GetHTTPReverseProxy"


async def serve():
    server = Server("Easegress")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=EasegressTools.ListHTTPReverseProxies,
                description="List all HTTP Reverse Proxies.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.CreateHTTPReverseProxy,
                description="Create a new HTTP Reverse Proxy.",
                inputSchema=schema.HTTPReverseProxySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.DeleteHTTPReverseProxy,
                description="Delete an HTTP Reverse Proxy.",
                inputSchema=schema.NameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.UpdateHTTPReverseProxy,
                description="Update an HTTP Reverse Proxy.",
                inputSchema=schema.HTTPReverseProxySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.GetHTTPReverseProxy,
                description="Get an HTTP Reverse Proxy.",
                inputSchema=schema.NameSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        logger.info(f"Call tool: {name}, arguments: {arguments}")

        if name == EasegressTools.ListHTTPReverseProxies:
            resp = await tools.list_http_reverse_proxies()
            return utils.to_textcontent(resp)

        elif name == EasegressTools.CreateHTTPReverseProxy:
            resp = await tools.create_http_reverse_proxy(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.DeleteHTTPReverseProxy:
            resp = await tools.delete_http_reverse_proxy(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.UpdateHTTPReverseProxy:
            resp = await tools.update_http_reverse_proxy(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.GetHTTPReverseProxy:
            resp = await tools.get_http_reverse_proxy(arguments)
            return utils.to_textcontent(resp)

        else:
            raise ValueError(f"Unknown tool name: {name}")

    return server


def run():
    async def _run():
        server = await serve()
        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, options, raise_exceptions=True)

    asyncio.run(_run())
