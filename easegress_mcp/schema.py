from typing import Optional, Dict
from pydantic import BaseModel
from enum import Enum


class EmptySchema(BaseModel):
    pass


class NameSchema(BaseModel):
    name: str


class IPFilter(BaseModel):
    blockByDefault: Optional[bool] = None
    allowIPs: Optional[list[str]] = None
    blockIPs: Optional[list[str]] = None


class Host(BaseModel):
    isRegexp: Optional[bool] = None
    value: str


class Path(BaseModel):
    path: str = ""
    pathPrefix: str = ""
    backend: str = ""

    # Placeholders for future use
    ipFilter: Optional[IPFilter] = None
    pathRegexp: Optional[str] = None
    rewriteTarget: Optional[str] = None
    methods: Optional[list[str]] = None
    clientMaxBodySize: Optional[int] = None
    headers: Optional[list[Dict]] = None
    queries: Optional[list[Dict]] = None
    matchAllHeader: Optional[bool] = None
    matchAllQuery: Optional[bool] = None


class Rule(BaseModel):
    host: str = ""
    paths: list[Path] = []

    # Placeholders for future use
    ipFilter: Optional[Dict] = None
    hostRegexp: Optional[str] = None
    hosts: Optional[list[Host]] = None


class HTTPServer(BaseModel):
    # Required field
    kind: str = "HTTPServer"
    name: str
    port: int

    rules: list[Rule] = []

    # Placeholders for future use
    http3: Optional[bool] = None
    keepAlive: Optional[bool] = None
    https: Optional[bool] = None
    autoCert: Optional[bool] = None
    xForwardedFor: Optional[bool] = None
    address: Optional[str] = None
    clientMaxBodySize: Optional[int] = None
    keepAliveTimeout: Optional[str] = None
    maxConnections: Optional[int] = None
    cacheSize: Optional[int] = None
    caCertBase64: Optional[str] = None
    certBase64: Optional[str] = None
    keyBase64: Optional[str] = None
    certs: Optional[Dict[str, str]] = None
    keys: Optional[Dict[str, str]] = None
    routerKind: Optional[str] = None
    ipFilter: Optional[IPFilter] = None
    globalFilter: Optional[str] = None
    accessLogFormat: Optional[str] = None


class PipelineFlowNode(BaseModel):
    filter: str
    # jumpIf


class PipelineFilter(BaseModel):
    kind: str
    name: str


class PoolServer(BaseModel):
    url: str


class ProxyPool(BaseModel):
    servers: list[PoolServer]


class ProxyFilter(PipelineFilter):
    pools: list[ProxyPool]


class Pipeline(BaseModel):
    name: str
    kind: str = "Pipeline"
    flow: list[PipelineFlowNode] = []
    filters: list[dict] = []


# Use common simplest fields for the time being
class AutoCertDNSProvider(BaseModel):
    name: str
    zone: str
    apiToken: str


class AutoCertDomain(BaseModel):
    name: str
    dnsProvider: AutoCertDNSProvider


class AutoCertManager(BaseModel):
    name: str
    kind: str = "AutoCertManager"
    email: str
    enableHTTP01: bool = True
    enableDNS01: bool = True
    enableTLSALPN01: bool = True
    domains: list[AutoCertDomain] = []


class LetsEncryptSchema(BaseModel):
    email: str = ""
    domainName: str = ""

    class DNSProviderNameEnum(str, Enum):
        cloudflare = "cloudflare"
        digitalocean = "digitalocean"
        dnspod = "dnspod"
        duckdns = "duckdns"
        vultr = "vultr"

    dnsProviderName: DNSProviderNameEnum = DNSProviderNameEnum.cloudflare
    dnsProviderZone: str = ""
    dnsProviderAPIToken: str = ""


class HTTPReverseProxySchema(BaseModel):
    name: str = "default_proxy"
    port: int = 80

    host: str = ""
    path: str = "/"
    isPathPrefix: bool = False
    endpoints: list[str] = []
