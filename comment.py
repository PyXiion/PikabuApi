from aiohttp import ClientSession
from .types.response.comment import Comment as CommentPayload
from .user import User
from datetime import datetime
from pikabu.request import make_request

class Comment:
  def __init__(self, session: ClientSession, user_id: int | None, payload: CommentPayload) -> None:
    self._session = session
    self._user_id = user_id

    # Main info
    self._id = payload["comment_id"]
    self._parent_id = payload["parent_id"]
    self._story_id = payload["story_id"]
    self._time = datetime.fromtimestamp(payload["comment_time"])

    self._content = payload["comment_desc"]

    # Statistics
    self._pluses = payload["comment_pluses"]
    self._minuses = payload["comment_minuses"]
    self._rating = payload["comment_rating"]

    # Author
    self._author = User(self._session, payload["user_id"], payload["user_name"])
    self._is_user_profile_deleted = payload["user_profile_deleted"]
    self._is_user_community_moderator = payload["is_user_community_moderator"]
    self._is_user_pikabu_team = payload["is_user_pikabu_team"]
    self._is_ignored_user = payload["is_ignored_user"]
    self._is_moderator_username = payload["is_moderator_username"]

    # Flags
    self._is_deleted = payload["is_deleted"]
    self._is_hidden = payload["is_hidden"]
    self._is_hidden_comment = payload["is_hidden_comment"]
    self._is_official = payload["is_official"]

    # Unknown
    self._platform = payload["comment_platform"]

  async def reply(self, text: str) -> bool:
    if not self._user_id:
      raise RuntimeError("Not authed")
    response = await Comment.create(self._session, self.id, self._user_id, text, self.id)
    return 'comment' in response

  @staticmethod
  async def create(session: ClientSession, story_id: int, user_id: int, text: str, parent_id: int | None = None):
    from pikabu.types.create_comment_query import CreateCommentQuery
    query: CreateCommentQuery = {
      "story_id": story_id,
      "user_id": user_id,
      "desc": text,
      "plain_text": True
    }
    if parent_id:
      query["parent_id"] = parent_id
    return await make_request(session, "comment.create", query)

  @property
  def id(self):
    return self._id
  @property
  def parent_id(self):
    return self._parent_id
  @property
  def story_id(self):
    return self._story_id
  @property
  def time(self):
    return self._time
  # TODO .story property

  @property
  def pluses(self):
    return self._pluses
  @property
  def rating(self):
    return self._rating
  @property
  def minuses(self):
    return self._minuses

  @property
  def text(self):
    return self._content["text"]
  @property
  def images(self):
    return self._content["images"]
  @property
  def videos(self):
    return self._content["videos"]

  @property
  def is_deleted(self):
    return self._is_deleted
  @property
  def is_hidden(self):
    return self._is_hidden
  @property
  def is_hidden_comment(self):
    return self._is_hidden_comment
  @property
  def is_official(self):
    return self._is_official

  @property
  def author(self):
    return self._author
  @property
  def is_user_profile_deleted(self):
    return self._is_user_profile_deleted
  @property
  def is_user_community_moderator(self):
    return self._is_user_community_moderator
  @property
  def is_user_pikabu_team(self):
    return self._is_user_pikabu_team
  @property
  def is_ignored_user(self):
    return self._is_ignored_user
  @property
  def is_moderator(self):
    return self._is_moderator_username

  @property
  def platform(self):
    return self._platform