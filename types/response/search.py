from typing import TypedDict, List

from .story import Story as StoryPayload


class Search(TypedDict):
  data: List[StoryPayload]
  total_stories: int
  page: int
  hide_visited_stories: bool
  hidden_stories_count: int
  hidden_by_rating: int
  key: str