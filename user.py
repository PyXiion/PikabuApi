from aiohttp import ClientSession
from typing import TYPE_CHECKING
from .user_profile import Profile
from .error_codes import PikabuError

if TYPE_CHECKING:
  from .subscribers import UserSubscribers
  from .subscriptions import UserSubscriptions

class User:
  class DoesNotExists(PikabuError):
    def __init__(self, *args: object) -> None:
      super().__init__(*args)

  def __init__(self, session: ClientSession, id: int, name: str, profile: Profile = None):
    self.__session = session
    self.id = int(id)
    self.name = name

    self.__profile = profile

  def get_subscriptions(self) -> "UserSubscriptions":
    from .subscriptions import UserSubscriptions
    return UserSubscriptions(self.__session, self.id)
  
  def get_subscribers(self) -> "UserSubscribers":
    from .subscribers import UserSubscribers
    return UserSubscribers(self.__session, self.id)
  
  async def get_profile(self) -> "Profile":
    if not self.__profile:
      self.__profile = await Profile.get_by_user_name(self.__session, self.name)
    return self.__profile