from .comments_page import CommentsPage
from ..comment import Comment

class CommentsIterator:
  from .story import Story

  def __init__(self, story: Story, first_page: CommentsPage):
    self._story = story
    self._comments: list[Comment] = first_page.comments
    self._has_next = first_page.has_next_page

  def __aiter__(self):
    return self

  async def __anext__(self) -> Comment:
    if not self._comments and self._has_next:
      page = await self._story.get_next_page()
      self._comments = page.comments
      self._has_next = page.has_next_page
    elif not self._comments:
      raise StopAsyncIteration

    return self._comments.pop(0)