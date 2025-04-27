import os
import httpx


def get_header():
    return {}


def get_async_client():
    client = httpx.AsyncClient(headers=get_header())
    return client


def get_client():
    client = httpx.Client(headers=get_header())
    return client


client = get_client()
async_client = get_async_client()
