# Easegress MCP Server

## Prompt Examples

### HTTP Reverse Proxy

1. **Create Proxy1**
   > Create HTTP reverse proxy `proxy1` on port `8080` with host `mcp.megaease.com`, path prefix `/service1` and endpoint `http://localhost:8081`.

2. **Create Proxy2**
   > Create an HTTP reverse proxy named `proxy2` on port `8080` with path `/service2` and endpoint `http://localhost:8082`.

3. **Update Proxy2**
   > Update `proxy2` to use path `/service2-updated`, and endpoint `http://localhost:8084`.

4. **Get Proxy2 Details**
   > Get details of `proxy2`.

5. **Delete nonexistent Proxy3**
   > Delete `proxy3`.

6. **Delete Proxy2**
    > Delete `proxy2`.

7. **List All Proxies**
   > List all proxies.

### Let's Encrypt

1. **Apply Let's Encrypt**
   > Apply Let's Encrypt with email `service@megaease.com`, domain name `mcp.megaease.com`, DNS provider `cloudflare`, DNS zone `megaease.com`, and API token `token-001`.

2. **Update Let's Encrypt**
   > Update Let's Encrypt with DNS zone `updated.megaease.com`, and API token `updated-token-001`.

3. **Get Let's Encrypt Details**
    > Get Let's Encrypt config.

4. **Delete Let's Encrypt**
    > Delete Let's Encrypt.
