from .types.vote_query import NewVoteQuery, Vote, VoteType
from .request import make_request
from aiohttp import ClientSession

class Item:
  def __init__(self, session: ClientSession, id: int, type: VoteType, user_id: int):
    self._session = session
    self._id = id
    self._user_id = user_id
    self._vote_type = type

  @staticmethod
  async def vote_item_by_id(session: ClientSession, item_id: int, user_id: int, type: VoteType, vote: Vote):
    query: NewVoteQuery = {
      "user_id": user_id,
      "item_id": item_id,
      "type": type,
      "vote": vote
    }
    return await make_request(session, "vote.new", query)

  async def vote(self, vote: Vote) -> bool:
    await Item.vote_item_by_id(self._session, self._id, self._user_id, self._vote_type, vote)
    return True