from aiohttp import ClientSession
from pikabu.types.response.community import GetCommunity as GetCommunityPayload
from pikabu.types.community_query import CommunityQuery

class CommunityLink:
  def __init__(self, id: int, name: str, link: str) -> None:
    self.id = id
    self.name = name
    self.link = link


class Community:
  def __init__(self, session: ClientSession, payload: GetCommunityPayload, user_id: int | None = None) -> None:
    self._session = session
    self._user_id = user_id

    self._payload = payload

  @staticmethod
  async def _get_by_link_name(session: ClientSession, communty_link_name: str, user_id: int = None) -> GetCommunityPayload:
    query: CommunityQuery = {
      "name": communty_link_name
    }
    if user_id:
      query["user_id"] = user_id

    from pikabu.request import make_request
    return await make_request(session, "community.get", query)

  @staticmethod
  async def get_by_id(session: ClientSession, community_link_name: str, user_id: int = None):
    payload = await Community._get_by_link_name(session, community_link_name, user_id)
    return Community(session, payload, user_id)

  @property
  def id(self):
    return self._payload["id"]

  @property
  def link_name(self):
    return self._payload["link_name"]

  @property
  def name(self):
    return self._payload["name"]

  @property
  def description(self):
    return self._payload["description"]

  @property
  def rules(self):
    return self._payload["rules"]

  @property
  def restriction(self):
    return self._payload["restriction"]

  @property
  def raw_community_admin(self):
    return self._payload["community_admin"]

  @property
  def raw_community_moderators(self):
    return self._payload["community_moderators"]

  @property
  def raw_community_chiefs(self):
    return self._payload["community_chiefs"]

  # TODO community_admin, community_moderators, community_chiefs

  @property
  def url(self):
    return self._payload["url"]

  @property
  def avatar_url(self):
    return self._payload["avatar_url"]

  @property
  def bg_image_url(self):
    return self._payload["bg_image_url"]

  @property
  def tags(self):
    return self._payload["tags"]

  @property
  def is_locked(self):
    return self._payload["is_locked"]

  @property
  def is_nsfw(self):
    return self._payload["is_nsfw"]

  @property
  def locked_message(self):
    return self._payload["lock_message"]

  @property
  def stories_count(self):
    return self._payload["stories"]

  @property
  def subscribers_count(self):
    return self._payload["subscribers"]

  @property
  def is_ignored(self):
    return self._payload["is_ignored"]

  @property
  def is_subscribed(self):
    return self._payload["is_subscribed"]

  @property
  def is_preview(self):
    return self._payload["is_in_preview_mode"]