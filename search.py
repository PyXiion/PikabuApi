from aiohttp import ClientSession
from .request import make_request
from .story import Story
from functools import reduce, partial
import operator
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .types.search_query import SearchQuery
  from .types.response.search import Search as SearchResponse

class Search:
  CONTROLLER = "search"

  def __init__(self, session: ClientSession, query: "SearchQuery", pages_at_once: int = 1) -> None:
    self.__session = session
    self.__query = query
    self.__pages_at_once = pages_at_once
    self.page = 1
    self.total_stories = None
    self.has_next_page = True

    self.update_views = False

  async def get_page(self, page: int = 1) -> list[Story]:
    self.__query["page"] = page

    data: SearchResponse = await make_request(self.__session, self.CONTROLLER, self.__query)

    if page == 1:
      self.total_stories = data["total_stories"]

    if "data" in data and len(data["data"]) > 0:
      stories = list(map(lambda x: Story(self.__session, x), data["data"]))

      if self.update_views:
        await asyncio.gather(*[x.update_view_count() for x in stories])
      
      return stories
    else:
      self.has_next_page = False
      return None

  async def next_page(self) -> list[Story]:
    if not self.has_next_page:
      return None
    
    pages = await asyncio.gather(*[self.get_page(self.page + x) for x in range(self.__pages_at_once)])
    pages = list(filter(partial(operator.is_not, None), pages))
    
    self.page += self.__pages_at_once
    if len(pages) > 0:
      return reduce(operator.add, pages)
    return None
  
  def __aiter__(self):
    return SearchIterator(self)

class SearchIterator:
  def __init__(self, search: Search) -> None:
    self.__search = search
    self.stories: list[Story] = None

  async def __anext__(self) -> Story:
    if not self.stories or len(self.stories) == 0:
      self.stories = await self.__search.next_page()
    
    if self.stories:
      return self.stories.pop(0)
    raise StopAsyncIteration