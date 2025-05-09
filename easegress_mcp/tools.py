from typing import Dict, List
from easegress_mcp import egapis
from easegress_mcp import schema
from urllib.error import HTTPError

mcp_http_server_name_prefix = "mcp_http_server_"
mcp_pipeline_name_prefix = "mcp_pipeline_"
mcp_proxy_filter_name = "mcp_proxy"


async def guarantee_http_server_exists(port: int):
    http_server_name = mcp_http_server_name_prefix + str(port)
    try:
        http_server = await egapis.get_http_server(http_server_name)
    except HTTPError as e:
        if e.code == 404:
            http_server = schema.HTTPServer(
                name=http_server_name,
                kind="HTTPServer",
                port=port,
                rules=[],
            )
            await egapis.create_http_server(http_server)
        else:
            raise

    return http_server


async def mount_http_reverse_proxy(http_reverse_proxy: schema.HTTPReverseProxySchema):
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    http_server = await egapis.get_http_server(http_server_name)
    if not http_server:
        raise HTTPError(f"HTTP server {http_server_name} not found")

    pipeline = await egapis.get_pipeline(pipeline_name)
    if not pipeline:
        raise HTTPError(f"Pipeline {pipeline_name} not found")

    for rule in http_server.rules:
        for path in rule.paths:
            if path.backend == pipeline.name:
                return

    rule = schema.Rule(
        host=http_reverse_proxy.host,
        paths=[
            schema.Path(
                path=http_reverse_proxy.path,
                pathPrefix=http_reverse_proxy.isPathPrefix,
                backend=pipeline.name,
            )
        ],
    )
    http_server.rules.append(rule)
    await egapis.update_http_server(http_server)


async def unmount_http_reverse_proxy(http_reverse_proxy: schema.HTTPReverseProxySchema):
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    http_server = await egapis.get_http_server(http_server_name)
    if not http_server:
        raise HTTPError(f"HTTP server {http_server_name} not found")

    for rule in http_server.rules:
        for path in rule.paths:
            if path.backend == pipeline_name:
                rule.paths.remove(path)
                break

    await egapis.update_http_server(http_server)


async def list_http_reverse_proxies() -> list[schema.HTTPReverseProxySchema]:
    http_servers = await egapis.list_http_servers()
    pipelines = await egapis.list_pipelines()
    http_reverse_proxies = []

    for http_server in http_servers:
        if not http_server.name.startswith(mcp_http_server_name_prefix):
            continue

        for pipeline in pipelines:
            if not pipeline.name.startswith(mcp_pipeline_name_prefix):
                continue

            rule_host, rule_path, isPathPrefix = None, None, False
            for rule in http_server.rules:
                for path in rule.paths:
                    if path.backend != pipeline.name:
                        continue
                    rule_host = rule.host
                    rule_path = path.path
                    if path.pathPrefix is not None:
                        rule_path = path.pathPrefix
                        isPathPrefix = True

            endpoints = []
            for filter in pipeline.filters:
                if filter.kind != "Proxy":
                    continue
                for pool in filter.pools:
                    for server in pool.servers:
                        endpoints.append(server.url)

            http_reverse_proxies.append(
                schema.HTTPReverseProxySchema(
                    name=pipeline.name[len(mcp_pipeline_name_prefix) :],
                    port=http_server.port,
                    host=rule_host,
                    path=rule_path,
                    isPathPrefix=isPathPrefix,
                    endpoints=endpoints,
                )
            )
    return http_reverse_proxies


async def create_http_reverse_proxy(arguments: dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    guarantee_http_server_exists(http_reverse_proxy.port)

    try:
        pipeline = await egapis.get_pipeline(pipeline_name)
    except HTTPError as e:
        if e.code == 404:
            pipeline = schema.Pipeline(
                name=pipeline_name,
                kind="Pipeline",
                flow=[
                    schema.PipelineFlowNode(
                        filter=mcp_proxy_filter_name,
                    )
                ],
                filters=[
                    schema.ProxyFilter(
                        kind="Proxy",
                        name=mcp_proxy_filter_name,
                        pools=[
                            schema.ProxyPool(
                                servers=[
                                    schema.PoolServer(url=url)
                                    for url in http_reverse_proxy.endpoints
                                ]
                            )
                        ],
                    )
                ],
            )

            await egapis.create_pipeline(pipeline)
            mount_http_reverse_proxy(http_reverse_proxy)
        else:
            raise


async def delete_http_reverse_proxy(arguments: dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    try:
        unmount_http_reverse_proxy(http_reverse_proxy)
        await egapis.delete_pipeline(pipeline_name)
    except HTTPError as e:
        if e.code == 404:
            pass
        else:
            raise

    http_server = await egapis.get_http_server(http_server_name)
    if len(http_server) == 0:
        await egapis.delete_http_server(http_server_name)


async def update_http_reverse_proxy(arguments: dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    try:
        pipeline = await egapis.get_pipeline(pipeline_name)
        pipeline.filters[0].pools[0].servers = [
            schema.PoolServer(url=url) for url in http_reverse_proxy.endpoints
        ]
        await egapis.update_pipeline(pipeline)
    except HTTPError as e:
        if e.code == 404:
            raise
        else:
            raise


async def get_http_reverse_proxy(arguments: dict) -> schema.HTTPReverseProxySchema:
    name = arguments["name"]

    http_reverse_proxies = await list_http_reverse_proxies()

    for http_reverse_proxy in http_reverse_proxies:
        if http_reverse_proxy.name == name:
            return http_reverse_proxy

    raise Exception(f"HTTP Reverse Proxy {name} not found")
