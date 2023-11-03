from pikabu.types.response.comment import Comment as CommentPayload
from pikabu.comment import Comment
from aiohttp import ClientSession

class CommentsPage:
  def __init__(self, session: ClientSession, user_id: int | None, comments_payload: list[CommentPayload], has_next_page: bool = False):
    self._comments = [Comment(session, user_id, payload) for payload in comments_payload]
    self._has_next_page = has_next_page

  @property
  def comments(self):
    return self._comments

  @property
  def has_next_page(self):
    return self._has_next_page