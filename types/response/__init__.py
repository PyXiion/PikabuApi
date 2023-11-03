from typing import TypedDict, Optional

from .error import Error as ErrorPayload


class Response(TypedDict):
  response: Optional[any]
  error: Optional[ErrorPayload]
  