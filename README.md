# Easegress MCP Server

## Features

- HTTP Reverse Proxy
- Let's Encrypt

## Setup

### Install

```bash
git clone https://github.com/megaease/easegress-mcp.git
pip install "mcp[cli]"
```

### Run on Cline

Change `${absolute_dir}` to the absolute path of the project directory and add the config below to the Cline MCP Servers.

```json
{
  "mcpServers": {
    "easegress_server": {
      "disabled": false,
      "timeout": 60,
      "command": "uv",
      "args": [
        "--directory",
        "${absolute_dir}/easegress-mcp",
        "run",
        "easegress_mcp/main.py"
      ],
      "env": {},
      "transportType": "stdio"
    },
}
```

## Prompt Examples

### HTTP Reverse Proxy

1. **Create Proxy1**
   > Add a proxy `proxy1` on port `8080` with host `mcp.megaease.com`, path prefix `/service1` and endpoint `http://localhost:8081`.

2. **Create Proxy2**
   > Add a proxy `proxy2` on port `8080` for path `/service2` with endpoint `http://localhost:8082`.

3. **Update Proxy2**
   > Change `proxy2` to `/service2-updated` and point it to `http://localhost:8084`.

4. **Get Proxy2 Details**
   > Show me the details of `proxy2`.

5. **Delete Proxy3**
   > Remove `proxy3`.

6. **Delete Proxy2**
   > Remove `proxy2`.

7. **List All Proxies**
   > Show all proxies.

### Let's Encrypt

1. **Apply Let's Encrypt**
   > Set up Let's Encrypt with email `service@megaease.com`, domain name `mcp.megaease.com`, DNS provider `cloudflare`, DNS zone `megaease.com`, and API token `token-001`.

2. **Update Let's Encrypt**
   > Update Let's Encrypt with DNS zone `updated.megaease.com` and token `updated-token-001`.

3. **Get Let's Encrypt Details**
   > Show the current Let's Encrypt config.

4. **Delete Let's Encrypt**
   > Remove the Let's Encrypt config.
