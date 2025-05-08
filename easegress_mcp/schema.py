from typing import Optional, Dict, List
from pydantic import BaseModel


class EmptySchema(BaseModel):
    pass


class NameSchema(BaseModel):
    name: str


class IPFilter(BaseModel):
    blockByDefault: Optional[bool] = None
    allowIPs: Optional[List[str]] = None
    blockIPs: Optional[List[str]] = None


class Host(BaseModel):
    isRegexp: Optional[bool] = None
    value: str


class Path(BaseModel):
    ipFilter: Optional[IPFilter] = None
    path: Optional[str] = None
    pathPrefix: Optional[str] = None
    pathRegexp: Optional[str] = None
    rewriteTarget: Optional[str] = None
    methods: Optional[List[str]] = None
    backend: Optional[str] = None
    clientMaxBodySize: Optional[int] = None
    headers: Optional[List[Dict]] = None
    queries: Optional[List[Dict]] = None
    matchAllHeader: Optional[bool] = None
    matchAllQuery: Optional[bool] = None


class Rule(BaseModel):
    ipFilter: Optional[Dict] = None
    host: Optional[str] = None
    hostRegexp: Optional[str] = None
    hosts: Optional[List[Host]] = None
    paths: Optional[List[Path]] = None


class HTTPServer(BaseModel):
    # Required field
    kind: str = "HTTPServer"
    name: str
    port: int

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
    rules: Optional[List[Rule]] = None
    globalFilter: Optional[str] = None
    accessLogFormat: Optional[str] = None


class PipelineFlowNode(BaseModel):
    filter: str
    # jumpIf


class PipelineFilter(BaseModel):
    name: str
    kind: str


class PoolServer(BaseModel):
    url: str


class ProxyPool(BaseModel):
    servers: List[PoolServer]


class ProxyFilter(PipelineFilter):
    pools: List[ProxyPool]


class Pipeline(BaseModel):
    name: str
    kind: str = "Pipeline"
    flow: List[PipelineFlowNode]
    filters: List[PipelineFilter]


class LetsEncryptSchema(BaseModel):
    letsEncrypt: bool = False
    letsEncryptEmail: str = ""
    letsEncryptDomainName: str = ""


class HTTPReverseProxySchema(BaseModel):
    name: str = "default_proxy"
    port: int = 80

    host: str = ""
    path: str = "/"
    isPathPrefix: bool = False
    endpoints: List[str] = []
