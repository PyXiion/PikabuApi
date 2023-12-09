from aiohttp import ClientSession
from datetime import datetime
from ..types.response.get_story import GetStory as GetStoryPayload
from ..types.story_query import StoryQuery
from ..item import Item
from ..community import Community
from ..user import User
from ..request import make_request
from .comments_page import CommentsPage


class Story(Item):
  def __init__(self, session: ClientSession, payload: GetStoryPayload, user_id: int | None = None) -> None:
    story_payload = payload["story"]
    self._session = session
    self._user_id = user_id

    super().__init__(self._session, story_payload["story_id"], "story", self._user_id)

    self.id = story_payload["story_id"]
    self.title = story_payload["story_title"]
    self.parent_id = story_payload["parent_story_id"]
    self.url = story_payload["story_url"]
    self.time = datetime.fromtimestamp(story_payload["story_time"])

    self.content = story_payload["story_data"]

    self.pluses = story_payload["story_pluses"]
    self.rating = story_payload["story_digs"]
    self.minuses = story_payload["story_minuses"]
    self.comments_count = story_payload["comments_count"]

    self.tags = story_payload["tags"]

    self.is_authors = story_payload["is_authors"]
    self.is_nsfw = story_payload["is_adult"]
    self.is_longpost = story_payload["is_longpost"]
    self.is_unique_author_story = story_payload["is_unique_author_story"]
    self.is_deleted = story_payload["is_deleted"]
    self.is_comment_disabled = story_payload["is_comm_disabled"]
    self.is_hot_comments = story_payload["is_hot_comments"]

    self.has_author_comments = story_payload["has_author_comments"]
    self.can_donate = story_payload["can_donate"]

    if self.is_unique_author_story:
      self.tags.insert(0, "Уникальная авторская история")
    if self.is_authors:
      self.tags.insert(0, "моё")
    if self.is_nsfw:
      self.tags.insert(0, "NSFW")

    self.tags = set(self.tags)

    self.community = Community(story_payload["community_id"], story_payload["community_name"],
                               story_payload["community_link"])
    self.author = User(self._session, story_payload["user_id"], story_payload["user_name"])

    self.views_count = None

    # Comments
    self._has_next_comments_page = payload["has_next_page_comments"]
    self._current_page = 1
    self._comment_pages: dict[int, CommentsPage] = {
      1: CommentsPage(self._session, self._user_id, payload["comments"], self._has_next_comments_page)
    }

  async def get_next_page(self) -> CommentsPage | None:
    if not self._has_next_comments_page:
      return None
    self._current_page += 1
    return await self.get_comments_page(self._current_page)

  async def get_comments_page(self, page: int) -> CommentsPage | None:
    if page in self._comment_pages:
      return self._comment_pages[page]

    data = await Story._get_by_id(self._session, self.id, self._user_id, page)
    comments = data["comments"]
    if len(comments) == 0:
      return None

    return CommentsPage(self._session, self._user_id, comments, data["has_next_page_comments"])

  @property
  def comments(self):
    from .comments_iterator import CommentsIterator
    return CommentsIterator(self, self._comment_pages[1])

  @staticmethod
  async def _get_by_id(session: ClientSession, story_id: int, user_id: int = None, page: int = 1) -> GetStoryPayload:
    query: StoryQuery = {
      "story_id": story_id,
      "page": page
    }
    if user_id:
      query["user_id"] = user_id

    return await make_request(session, "story.get", query)

  @staticmethod
  async def get_by_id(session: ClientSession, story_id: int, user_id: int = None, page: int = 1) -> "Story":
    payload = await Story._get_by_id(session, story_id, user_id, page)
    return Story(session, payload, user_id)

  @staticmethod
  async def get_views_by_id(session: ClientSession, story_id: int):
    async with session.get(f"https://d.pikabu.ru/stat/story/{story_id}") as resp:
      data = await resp.json(encoding="utf-8")
      return data['data']['v']

  async def update_view_count(self) -> int:
    self.views_count = await Story.get_views_by_id(self._session, self.id)
    return self.views_count

  async def comment(self, text: str) -> bool:
    if not self._user_id:
      raise RuntimeError("Not authed")
    
    from ..comment import Comment
    response = await Comment.create(self._session, self.id, self._user_id, text)
    return 'comment' in response