from typing import TypedDict, List
from pikabu.types.response.story import Story
from pikabu.types.response.comment import Comment

class GetStory(TypedDict):
  # Story
  story: Story

  # Comments
  comments: List[Comment]
  has_next_page_comments: bool