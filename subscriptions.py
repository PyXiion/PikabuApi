from aiohttp import ClientSession
from typing import TYPE_CHECKING

from .community import Community
from .user import User

class UserSubscriptions:
  def __init__(self, session: ClientSession, user_id: int) -> None:
    self.__session = session
    self.__user_id = user_id
    self.__page = 0
    self.__has_next = True

    self.__users = []
    self.__communities = []

  async def fetch_next_page(self) -> bool:
    if self.__has_next:
      self.__page += 1

      params = {
        "route": "user/subscriptions",
        "user_id": self.__user_id,
        "page": self.__page
      }
      async with self.__session.get("https://pikabu.ru/ajax.php", params=params) as response:
        data = await response.json()
        
        if data['result']:
          data = data['data']
          users: list[dict] = data['users']
          communities: list[dict] = data['communities']

          if len(users) > 0:
            self.__users += list(map(lambda x: User(x["id"], x["name"]), users))
          if len(communities) > 0:
            self.__communities += list(map(lambda x: Community(x["id"], x["name"]), communities))

          self.__has_next = data['has_more']
        else:
          self.__has_next = False

      return self.__has_next
    
    return False

  async def fetch_all_pages(self):
    while await self.fetch_next_page(): 
      pass
  
  def get_users(self) -> list[User]:
    return list(self.__users)
  
  def get_communities(self) -> list[Community]:
    return list(self.__communities)  