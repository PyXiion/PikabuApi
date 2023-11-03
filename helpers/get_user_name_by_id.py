from aiohttp import ClientSession
from bs4 import BeautifulSoup

ACTION = 'get_short_profile'
HEADERS = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
}

class UnknownGetUserNameByIdError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

async def get_user_name_by_id(session: ClientSession, user_id):
  async with session.post('https://pikabu.ru/ajax/user_info.php', params={
    "action": ACTION,
    "user_id": user_id
  }, headers=HEADERS) as resp:
    data = await resp.json()
    
    if not data['result']:
      from ..user import User

      raise User.DoesNotExists("Пользователь не существует!")
    if 'data' not in data:
      raise UnknownGetUserNameByIdError
    
    html = data['data']['html']
    soup = BeautifulSoup(html, 'html.parser')

    nick = soup.find(class_='profile__nick').a.string

    return nick