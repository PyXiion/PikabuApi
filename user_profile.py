from typing import TYPE_CHECKING
from aiohttp import ClientSession
from .request import make_request
from datetime import datetime
if TYPE_CHECKING:
  from .types.profile_query import ProfileQuery
  from .types.response.profile import Profile as ProfilePayload

class Profile:
  def __init__(self, payload: "ProfilePayload") -> None:
    user = payload["user"]
    self.id: int = int(user["user_id"])
    self.name: str = user["user_name"]
    self.about: str = user["about"]
    self.gender: int = user["gender"]

    self.registration_duration = user["registration_duration"]
    self.signup_date = datetime.fromtimestamp(int(user["signup_date"]))

    self.public_ban_history = user["public_ban_history"]

    self.subscribers_count: int = user["subscribers_count"]
    self.comments_count: int = user["comments_count"]
    self.stories_count: int = user["stories_count"]
    self.stories_hot_count: int = user["stories_hot_count"]
    self.stories_queue_count: int = user["stories_queue_count"]
    self.pluses_count: int = user["pluses_count"]
    self.minuses_count: int = user["minuses_count"]

    self.edit_changes_count = user["cedit_changes_count"]
    self.edit_votes_count = user["cedit_votes_count"]

    self.rating: float = user["rating"]

    self.is_rating_ban: bool = user["is_rating_ban"]
    self.is_banned: bool = user["is_user_banned"]
    self.is_fully_banned: bool = user["is_user_fully_banned"]
    self.is_show_extended_profile: bool = user["is_show_extended_profile"]
    self.is_advert_blogs: bool = user["is_advert_blogs_user"]
    self.header_bg_forbidden = user["header_bg_forbidden"]

    self.is_slow_mode_enabled = user["is_slow_mode_enabled"]
    self.slow_mode_text = user["slow_mode_text"]

    self.approved: bool = user["approved"]

  async def get_by_user_name(session: ClientSession, username: str, user_id: int = None) -> "Profile":
    query: ProfileQuery = {
      "user_name": username
    }
    if user_id:
      query["user_id"] = user_id

    data = await make_request(session, "user.profile.get", query)

    payload: ProfilePayload = data

    return Profile(payload)