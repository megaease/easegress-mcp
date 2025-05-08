from typing import Dict, List
from easegress_mcp import egapis
from easegress_mcp import schema
from urllib.error import HTTPError

mcp_http_server_name_prefix = "mcp_http_server_"
mcp_pipeline_name_prefix = "mcp_pipeline_"
mcp_proxy_filter_name = "mcp_proxy"


def guarantee_http_server_exists(port: int):
    http_server_name = mcp_http_server_name_prefix + str(port)
    try:
        http_server = egapis.get_http_server(http_server_name)
    except HTTPError as e:
        if e.code == 404:
            http_server = schema.HTTPServer(
                name=http_server_name,
                kind="HTTPServer",
                port=port,
                rules=[],
            )
            egapis.create_http_server(http_server)
        else:
            raise

    return http_server


def mount_http_reverse_proxy(http_reverse_proxy: schema.HTTPReverseProxySchema):
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    http_server = egapis.get_http_server(http_server_name)
    if not http_server:
        raise HTTPError(f"HTTP server {http_server_name} not found")

    pipeline = egapis.get_pipeline(pipeline_name)
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
    egapis.update_http_server(http_server)


def unmount_http_reverse_proxy(http_reverse_proxy: schema.HTTPReverseProxySchema):
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    http_server = egapis.get_http_server(http_server_name)
    if not http_server:
        raise HTTPError(f"HTTP server {http_server_name} not found")

    for rule in http_server.rules:
        for path in rule.paths:
            if path.backend == pipeline_name:
                rule.paths.remove(path)
                break

    egapis.update_http_server(http_server)


def list_http_reverse_proxies():
    http_servers = egapis.list_http_servers()
    pipelines = egapis.list_pipelines()
    http_reverse_proxies = []
    for http_server in http_servers:
        if not http_server.name.startswith(mcp_http_server_name_prefix):
            continue

        for pipeline in pipelines:
            if not pipeline.name.startswith(mcp_pipeline_name_prefix):
                return

            host, path, isPathPrefix = None, None, False
            for rule in http_server.rules:
                for path in rule.paths:
                    if path.backend != pipeline.name:
                        continue
                    host = rule.host
                    path = path.path
                    if path.pathPrefix is not None:
                        path = path.pathPrefix
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
                    name=pipeline.name,
                    port=http_server.port,
                    host=host,
                    path=path,
                    isPathPrefix=isPathPrefix,
                    endpoints=endpoints,
                )
            )


def create_http_reverse_proxy(arguments: Dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    guarantee_http_server_exists(http_reverse_proxy.port)

    try:
        pipeline = egapis.get_pipeline(pipeline_name)
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
                        name=mcp_proxy_filter_name,
                        kind="Proxy",
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
            egapis.create_pipeline(pipeline)
            mount_http_reverse_proxy(http_reverse_proxy)
        else:
            raise


def delete_http_reverse_proxy(arguments: Dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    try:
        unmount_http_reverse_proxy(http_reverse_proxy)
        egapis.delete_pipeline(pipeline_name)
    except HTTPError as e:
        if e.code == 404:
            pass
        else:
            raise

    http_server = egapis.get_http_server(http_server_name)
    if len(http_server) == 0:
        egapis.delete_http_server(http_server_name)


def update_http_reverse_proxy(arguments: Dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    try:
        pipeline = egapis.get_pipeline(pipeline_name)
        pipeline.filters[0].pools[0].servers = [
            schema.PoolServer(url=url) for url in http_reverse_proxy.endpoints
        ]
        egapis.update_pipeline(pipeline)
    except HTTPError as e:
        if e.code == 404:
            raise
        else:
            raise


def get_http_reverse_proxy(arguments: Dict) -> schema.HTTPReverseProxySchema:
    name = arguments["name"]

    pipeline_name = mcp_pipeline_name_prefix + name
    return egapis.get_pipeline(pipeline_name)
