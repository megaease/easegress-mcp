from typing import Dict, List
from easegress_mcp import egapis
from easegress_mcp import schema
from urllib.error import HTTPError

mcp_http_server_name_prefix = "mcp_http_server_"
mcp_pipeline_name_prefix = "mcp_pipeline_"
mcp_proxy_filter_name = "mcp_proxy"

# HTTP Reverse Proxy part.


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

    pipeline_rule = schema.Rule(
        host=http_reverse_proxy.host,
        paths=[
            schema.Path(
                path=http_reverse_proxy.path
                if not http_reverse_proxy.isPathPrefix
                else "",
                pathPrefix=http_reverse_proxy.path
                if http_reverse_proxy.isPathPrefix
                else "",
                backend=pipeline.name,
            )
        ],
    )

    for rule in http_server.rules:
        for path in rule.paths:
            if path.backend == pipeline.name:
                rule.host = pipeline_rule.host
                rule.paths = pipeline_rule.paths
                await egapis.update_http_server(http_server)
                return

    http_server.rules.append(pipeline_rule)

    await egapis.update_http_server(http_server)


async def unmount_http_reverse_proxy(http_reverse_proxy: schema.HTTPReverseProxySchema):
    http_server_name = mcp_http_server_name_prefix + str(http_reverse_proxy.port)
    pipeline_name = mcp_pipeline_name_prefix + http_reverse_proxy.name

    http_server = await egapis.get_http_server(http_server_name)

    for rule in http_server.rules:
        for path in rule.paths:
            if path.backend == pipeline_name:
                http_server.rules.remove(rule)
                break

    if (
        http_server.name.startswith(mcp_http_server_name_prefix)
        and len(http_server.rules) == 0
    ):
        print(f"HTTP server {http_server.name} has no rules, deleting it")
        await egapis.delete_http_server(http_server.name)
        return

    await egapis.update_http_server(http_server)


async def list_http_reverse_proxies() -> list[schema.HTTPReverseProxySchema]:
    http_servers = await egapis.list_http_servers()
    pipelines = await egapis.list_pipelines()
    http_reverse_proxies = []

    for pipeline in pipelines:
        if not pipeline.name.startswith(mcp_pipeline_name_prefix):
            continue

        for http_server in http_servers:
            if not http_server.name.startswith(mcp_http_server_name_prefix):
                continue

            rule_host, rule_path, isPathPrefix = "", "", False
            found = False
            for rule in http_server.rules:
                for path in rule.paths:
                    if path.backend != pipeline.name:
                        continue
                    found = True
                    rule_host = rule.host
                    rule_path = path.path
                    if len(path.pathPrefix) > 0:
                        rule_path = path.pathPrefix
                        isPathPrefix = True

            if not found:
                continue

            endpoints = []
            for filter in pipeline.filters:
                if filter["kind"] != "Proxy":
                    continue
                for pool in filter["pools"]:
                    for server in pool["servers"]:
                        endpoints.append(server["url"])

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

    await guarantee_http_server_exists(http_reverse_proxy.port)

    pipeline = schema.Pipeline(
        name=pipeline_name,
        kind="Pipeline",
        flow=[
            schema.PipelineFlowNode(
                filter=mcp_proxy_filter_name,
            )
        ],
        filters=[
            {
                "kind": "Proxy",
                "name": mcp_proxy_filter_name,
                "pools": [
                    {
                        "servers": [
                            schema.PoolServer(url=url)
                            for url in http_reverse_proxy.endpoints
                        ]
                    }
                ],
            }
        ],
    )

    try:
        await egapis.create_pipeline(pipeline)
    except HTTPError as e:
        if e.code == 409:
            raise HTTPError(
                e.url,
                e.code,
                f"Proxy {http_reverse_proxy.name} already exists",
                None,
                None,
            )
        else:
            raise

    await mount_http_reverse_proxy(http_reverse_proxy)


async def delete_http_reverse_proxy(arguments: dict):
    name = arguments["name"]
    pipeline_name = mcp_pipeline_name_prefix + name
    http_servers = await egapis.list_http_servers()

    try:
        await egapis.delete_pipeline(pipeline_name)
    except HTTPError as e:
        if e.code == 404:
            raise HTTPError(e.url, e.code, f"Proxy {name} not found", None, None)
        else:
            raise

    for http_server in http_servers:
        http_reverse_proxy = schema.HTTPReverseProxySchema(
            name=name,
            port=http_server.port,
        )
        await unmount_http_reverse_proxy(http_reverse_proxy)


async def update_http_reverse_proxy(arguments: dict):
    http_reverse_proxy = schema.HTTPReverseProxySchema(**arguments)

    await delete_http_reverse_proxy({"name": http_reverse_proxy.name})
    await create_http_reverse_proxy(arguments)
    return

    # FIXME: Store pipeline info in pipeline itself to avoid
    # complicated link logic between HTTPServer and Pipeline.

    # pipeline = await egapis.get_pipeline(pipeline_name)
    # for filter in pipeline.filters:
    #     if filter["kind"] != "Proxy":
    #         continue
    #     filter["pools"] = [
    #         {
    #             "servers": [
    #                 schema.PoolServer(url=url) for url in http_reverse_proxy.endpoints
    #             ]
    #         }
    #     ]
    # await egapis.update_pipeline(pipeline)
    # await guarantee_http_server_exists(http_reverse_proxy.port)
    # await mount_http_reverse_proxy(http_reverse_proxy)


async def get_http_reverse_proxy(arguments: dict) -> schema.HTTPReverseProxySchema:
    name = arguments["name"]

    http_reverse_proxies = await list_http_reverse_proxies()

    for http_reverse_proxy in http_reverse_proxies:
        if http_reverse_proxy.name == name:
            return http_reverse_proxy

    raise Exception(f"Proxy {name} not found")


# Let's Encrypt part.


async def apply_lets_encrypt(arguments: dict):
    lets_encrypt = schema.LetsEncryptSchema(**arguments)
    dns_provider = schema.AutoCertDNSProvider(
        name=lets_encrypt.dnsProviderName,
        zone=lets_encrypt.dnsProviderZone,
        apiToken=lets_encrypt.dnsProviderAPIToken,
    )
    domain = schema.AutoCertDomain(
        name=lets_encrypt.domainName, dnsProvider=dns_provider
    )
    auto_cert_manager = schema.AutoCertManager(
        name="AutoCertManager",
        kind="AutoCertManager",
        email=lets_encrypt.email,
        enableHTTP01=True,
        enableDNS01=True,
        enableTLSALPN01=True,
        domains=[domain],
    )

    try:
        await egapis.get_auto_cert_manager()
    except HTTPError as e:
        if e.code == 404:
            await egapis.create_auto_cert_manager(auto_cert_manager)
        else:
            raise

    await egapis.update_auto_cert_manager(auto_cert_manager)


async def delete_lets_encrypt(arguments: dict):
    auto_cert_manager_name = "AutoCertManager"
    try:
        await egapis.delete_auto_cert_manager()
    except HTTPError as e:
        if e.code == 404:
            raise HTTPError(
                e.url,
                e.code,
                f"AutoCertManager {auto_cert_manager_name} not found",
                None,
                None,
            )
        else:
            raise


async def get_lets_encrypt(arguments: dict) -> schema.AutoCertManager:
    try:
        auto_cert_manager = await egapis.get_auto_cert_manager()
    except HTTPError as e:
        if e.code == 404:
            raise HTTPError(e.url, e.code, "AutoCertManager not found", None, None)
        else:
            raise

    return auto_cert_manager
