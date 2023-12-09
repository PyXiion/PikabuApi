from typing import TypedDict, Literal

VoteType = Literal["comment", "story"]
Vote = Literal[-1, 0, 1]

class NewVoteQuery(TypedDict):
  type: VoteType
  vote: Vote
  item_id: int
  user_id: int