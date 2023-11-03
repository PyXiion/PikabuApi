from typing import TypedDict, Optional
from enum import Enum
from datetime import date

class SearchSort(Enum):
  NEW = 1
  BEST = 2
  RELEVANCE = 3

class SearchQuery(TypedDict):
  text: Optional[str]
  rating: Optional[int]
  tags: Optional[str]
  user: Optional[str]
  community: Optional[str]
  date_from: Optional[int]
  date_to: Optional[int]
  sort: Optional[SearchSort]
  
  page: int
  user_id: Optional[int]