import asyncio
from enum import Enum
from typing import List

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server

from easegress_mcp import egapis
from easegress_mcp import utils
from easegress_mcp import schema
from easegress_mcp.log import logger


class EasegressTools(str, Enum):
    ListHTTPServers = "list_HTTPServers"
    CreateHTTPServer = "create_HTTPServer"
    DeleteHTTPServer = "delete_HTTPServer"
    UpdateHTTPServer = "update_HTTPServer"
    GetHTTPServer = "get_HTTPServer"

    ListProxyPipelines = "list_ProxyPipelines"
    CreateProxyPipeline = "create_ProxyPipeline"
    DeleteProxyPipeline = "delete_ProxyPipeline"
    UpdateProxyPipeline = "update_ProxyPipeline"
    GetProxyPipeline = "get_ProxyPipeline"


async def serve():
    server = Server("Easegress")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=EasegressTools.ListHTTPServers,
                description="List all HTTP servers.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.CreateHTTPServer,
                description="Create an HTTP server.",
                inputSchema=schema.HTTPServerSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.DeleteHTTPServer,
                description="Delete an HTTP server.",
                inputSchema=schema.NameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.UpdateHTTPServer,
                description="Update an HTTP server.",
                inputSchema=schema.HTTPServerSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.GetHTTPServer,
                description="Get an HTTP server.",
                inputSchema=schema.NameSchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.ListProxyPipelines,
                description="List all Proxy Pipelines.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.CreateProxyPipeline,
                description="Create a Proxy Pipeline.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.DeleteProxyPipeline,
                description="Delete a Proxy Pipeline.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.UpdateProxyPipeline,
                description="Update a Proxy Pipeline.",
                inputSchema=schema.EmptySchema.model_json_schema(),
            ),
            Tool(
                name=EasegressTools.GetProxyPipeline,
                description="Get a Proxy Pipeline.",
                inputSchema=schema.NameSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        logger.info(f"Call tool: {name}, arguments: {arguments}")

        if name == EasegressTools.ListHTTPServers:
            resp = await egapis.list_HTTPServers()
            return utils.to_textcontent(resp)

        elif name == EasegressTools.CreateHTTPServer:
            resp = await egapis.create_HTTPServer(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.DeleteHTTPServer:
            resp = await egapis.delete_HTTPServer(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.UpdateHTTPServer:
            resp = await egapis.update_HTTPServer(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.GetHTTPServer:
            resp = await egapis.get_HTTPServer(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.ListProxyPipelines:
            resp = await egapis.list_ProxyPipelines()
            return utils.to_textcontent(resp)

        elif name == EasegressTools.CreateProxyPipeline:
            resp = await egapis.create_ProxyPipeline(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.DeleteProxyPipeline:
            resp = await egapis.delete_ProxyPipeline(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.UpdateProxyPipeline:
            resp = await egapis.update_ProxyPipeline(arguments)
            return utils.to_textcontent(resp)

        elif name == EasegressTools.GetProxyPipeline:
            resp = await egapis.get_ProxyPipeline(arguments)
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
