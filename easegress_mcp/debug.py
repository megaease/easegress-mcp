import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easegress_mcp import tools


async def debug():
    # Step 1: Create three HTTP reverse proxies
    proxy1 = {
        "name": "proxy1",
        "port": 8080,
        "host": "localhost",
        "path": "/service1",
        "isPathPrefix": True,
        "endpoints": ["http://localhost:8081"],
    }
    proxy2 = {
        "name": "proxy2",
        "port": 8080,
        "host": "localhost",
        "path": "/service2",
        "isPathPrefix": True,
        "endpoints": ["http://localhost:8082"],
    }
    proxy3 = {
        "name": "proxy3",
        "port": 8080,
        "host": "localhost",
        "path": "/service3",
        "isPathPrefix": True,
        "endpoints": ["http://localhost:8083"],
    }

    await tools.create_http_reverse_proxy(proxy1)
    await tools.create_http_reverse_proxy(proxy2)
    await tools.create_http_reverse_proxy(proxy3)

    # Step 2: Update one of the proxies
    updated_proxy2 = {
        "name": "proxy2",
        "port": 8082,
        "host": "localhost",
        "path": "/service2-updated",
        "isPathPrefix": True,
        "endpoints": ["http://localhost:8084"],
    }
    await tools.update_http_reverse_proxy(updated_proxy2)

    # Step 3: Delete one of the proxies
    await tools.delete_http_reverse_proxy({"name": "proxy3"})

    # Step 4: List all remaining proxies
    remaining_proxies = await tools.list_http_reverse_proxies()
    print("Remaining Proxies:", remaining_proxies)

    # Step 5: Get details of a specific proxy
    proxy_details = await tools.get_http_reverse_proxy({"name": "proxy2"})
    print("Proxy2 Details:", proxy_details)
    arguments = {
        "name": "test",
        "port": 8080,
        "host": "localhost",
        "path": "/",
        "isPathPrefix": True,
        "endpoints": ["http://localhost:8081"],
    }

    await tools.create_http_reverse_proxy(arguments)


if __name__ == "__main__":
    # Use asyncio.run to execute the async debug function
    import asyncio  # Import asyncio to run the async function

    asyncio.run(debug())
