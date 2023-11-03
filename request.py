import aiohttp
from aiohttp import ClientSession
from .error_codes import create_error
from .logger import logger

def to_str(v):
  if type(v) == bool:
    return 'true' if v else 'false'
  return str(v)

def make_hash(params: dict[str, any], controller: str, ms: int, key: str) -> str:
  from hashlib import md5
  from base64 import b64encode

  values = sorted([to_str(x) for x in params.values()])
  to_hash: str = f"{key},{controller},{ms},{','.join(values)}"
  hash = md5(to_hash.encode()).hexdigest().encode()
  base64 = b64encode(hash)
  return base64.decode()

def make_request_body(controller: str, params: dict[str, any]) -> tuple[dict[str, any], int]:
  from time import time
  
  ms = int(round(time() * 1000))
  params["new_sort"] = 1
  hash = make_hash(params, controller, ms, "kmq4!2cPl)peZ")

  return params | {
    "token": ms,
    "id": "iws",
    "hash": hash
  }, ms

async def make_request(session: ClientSession, controller: str, params: dict[str, any]) -> dict[str, any]:
  logger.debug("make_request : " + str(locals()))
  json, _ = make_request_body(controller, params)

  logger.debug(f"json = {json}")

  async with session.post("https://api.pikabu.ru/v1/" + controller, json=json) as response:
    data = await response.json(encoding="utf-8")
    logger.debug(f"data = {data}")

    if 'response' in data:
      return data['response']

    message = data['error']['message']
    code = data['error']['message_code']

    logger.error(f"Request Error {code} - {message}")
    raise create_error(code, message)