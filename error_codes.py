from enum import IntEnum

class ErrorCode(IntEnum):
  NSFW = 47

  INCORRECT_LOGIN_DETAILS = 136

  NOT_FOUND = 404

class PikabuError(BaseException):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class NsfwError(PikabuError): # 47
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class IncorrectLoginDetailsError(PikabuError): # 136
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class NotFoundError(PikabuError): # 404
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class UnknownError(PikabuError):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

def create_error(error_code: int, *args: object):
  match error_code:
    case ErrorCode.NSFW:
      return NsfwError(*args)
    
    case ErrorCode.INCORRECT_LOGIN_DETAILS:
      return IncorrectLoginDetailsError(*args)
    
    case ErrorCode.NOT_FOUND:
      return NotFoundError(*args)
    
  raise UnknownError(*args)