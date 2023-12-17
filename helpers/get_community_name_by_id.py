import time

import aiohttp

HEADERS = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
  "Origin": "https://pikabu.ru",
  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
class UnknownGetCommunityNameByIdError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class TooManyRequests(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


def batch(iterable, size):
  arr = []
  for i in iterable:
    arr.append(i)

    if len(arr) == size:
      yield arr
      arr.clear()

  if arr:
    yield arr

async def get_community_name_by_id(com_ids: list[int], should_undo_action = True, cookies = {}):
  """
  Required auth
  """

  headers = HEADERS | {
    'Cookie': ' '.join([f'{k}={v};' for k, v in cookies.items()])
  }
  async with aiohttp.ClientSession(headers=headers) as session:
    com_names = []
    for ids in batch(com_ids, 10):
      params = {
        'authors': '',
        'communities': ','.join(map(str, ids)),
        'tags': '',
        'keywords': '',
        'story_id': '0',
        'period': 'week',
        'action': 'add_rule'
      }
      async with session.post(
          'https://pikabu.ru/ajax/ignore_actions.php',
          data=params, params=params,
          allow_redirects=False) as resp:
        data = await resp.json()

        if data['message_code'] == 4:
          raise TooManyRequests()

        if not data['result'] or 'data' not in data or not data['data']:
          from ..user import User

          raise User.DoesNotExists("Сообщество не существует!")  # FIXME

        data = data['data']
        com_names += data['communities']

        rule_id = data['id']

      if should_undo_action:
        params = {
          'action': 'remove_rule',
          'id': str(rule_id)
        }
        await session.post('https://pikabu.ru/ajax/ignore_actions.php', params=params)

  return {
    c["id"]: c["slug"] for c in com_names
  }