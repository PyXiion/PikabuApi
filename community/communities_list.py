from aiohttp import ClientSession
from bs4 import BeautifulSoup

class CommunityRef:
  def __init__(self, _id: int, name: str, link_name: str):
    self.id = _id
    self.name = name
    self.link_name = link_name

class CommunitiesList:
  URL: str = "https://pikabu.ru/ajax/communities_actions.php"
  HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
  }

  def __init__(self, session: ClientSession):
    self._session = session
    self._communities: list[CommunityRef] = []
    self._page = 1
    self._has_more = True

  def __aiter__(self):
    return self

  async def __anext__(self):
    if len(self._communities) == 0:
      if self._has_more:
        params = {
          "action": "get_communities",
          "sort": "time",
          "type": "all",
          "filterType": "all",
          "page": self._page
        }
        async with self._session.post(CommunitiesList.URL, params=params, headers=CommunitiesList.HEADERS) as response:
          data = await response.json(encoding='utf-8')
          if data["result"] == True:
            data = data["data"]
            self._has_more = data["has_more"]
            self._page += 1

            communities_html: list[str] = data["list"]

            for community_html in communities_html:
              soup = BeautifulSoup(community_html, 'html.parser')

              _id = int(soup.find()['data-id'])
              name = soup.find(class_='community__title').a.string
              link_name = soup.find(class_='community-avatar')['href'].split('/')[-1]

              self._communities.append(CommunityRef(_id, name, link_name))
      else:
        raise StopAsyncIteration

    return self._communities.pop(0)