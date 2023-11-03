from aiohttp import ClientSession
from yarl import URL
from random import randint
from datetime import date

from .user import User, Profile
from .search import Search
from .story import Story
from .request import make_request
import time
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .types.search_query import SearchQuery, SearchSort
  from .types.auth_query import AuthQuery
  from .types.response.auth import Auth as AuthPayload

logger = logging.getLogger("pikabu")

HEADERS = {
  "DeviceId": str(randint(0, 100_000_000)),
  "User-Agent": "ru.pikabu.android/1.21.15 (SM-N975F Android 7.1.2)"
}
COOKIES = {
  "unqKms867": "aba48a160c",
  "rm5bH": "8c68fbfe3dc5e5f5b23a9ec1a8f784f8"
}
DOMAIN = URL("https://api.pikabu.ru")

def get_ms(date: date) -> int:
  return int(round(time.mktime(date.timetuple()) * 1000))

def get_search_days(d: date) -> int:
  CACHE_PERIOD = 86400000
  DATE_FROM = get_ms(date(2008, 1, 1))
  ms = get_ms(d)
  
  return (ms - DATE_FROM) // CACHE_PERIOD

class Session:
  def __init__(self) -> None:
    self.__session = ClientSession(headers=HEADERS, cookies=COOKIES)
    self.__user_id = None

  async def __aenter__(self):
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close()

  async def close(self) -> None:
    logger.info("Сессия закрыта")
    await self.__session.close()

  def is_authed(self) -> bool:
    return self.__user_id is not None

  async def auth(self, login: str, password: str):
    query: AuthQuery = {
      "user_name": login,
      "password": password
    }
    data: AuthPayload = await make_request(self.__session, "user.auth", query)
    self.__user_id = data["user_id"]
  
  async def get_story(self, story_id: int) -> Story:
    return await Story.get_by_id(self.__session, story_id, self.__user_id)

  async def create_user_object(self, name: str, id: int) -> User:
    return User(self.__session, id, name)
  
  async def get_user_by_name(self, name: str) -> User:
    profile = await Profile.get_by_user_name(self.__session, name, self.__user_id)
    return User(self.__session, int(profile.id), profile.name, profile)
  
  async def get_user_by_id(self, id: int) -> User:
    from .helpers.get_user_name_by_id import get_user_name_by_id
    return User(self.__session, id, await get_user_name_by_id(self.__session, id))

  def search(self, *, 
                   text: str = None, 
                   rating: int = None, 
                   tags: list[str] | str = None, 
                   user: str = None, 
                   community: str = None, 
                   date_from: date = None, 
                   date_to: date = None,
                   sort: "SearchSort" = None,
                   pages_at_once: int = 1):
    query: SearchQuery = {}
    if (text):
      query["text"] = text
    if (rating):
      query["rating"] = rating
    if (tags):
      if type(tags) is str:
        query["tags"] = tags
      elif type(tags) is list:
        query["tags"] = ','.join(tags)
      else:
        raise RuntimeError("Invalid type for tags. It must be str or list.")
    if (user):
      query["user"] = user
    if (community):
      query["user"] = user
    if (sort):
      query["sort"] = sort.value

    if (date_from):
      query["date_from"] = get_search_days(date_from)
    if (date_to):
      query["date_from"] = get_search_days(date_to)

    if (self.__user_id):
      query["user_id"] = self.__user_id

    return Search(self.__session, query, pages_at_once)
  
  def load_session(self, data) -> None:
    self.__session.cookie_jar.update_cookies(data['cookies'])
    self.__session.headers.extend(data["headers"])

  def save_session(self) -> dict:
    return {
      'cookies': {k: v.value for k, v in self.__session.cookie_jar.filter_cookies(DOMAIN).items()},
      'headers': dict(self.__session.headers.items())
    }
  
  def get_session(self) -> ClientSession:
    return self.__session