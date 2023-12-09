# Pikabu API
Простой API для Пикабу написанный на Python. Сделан под свои личные нужды, поэтому не реализует весь функционал Пикабу и содержит говнокод.

## Как использовать
Создайте объект pikabu.Session и используйте его методы.

```py
from pikabu import Session
from asyncio import run
from random import randint

from pikabu.error_codes import IncorrectLoginDetailsError

async def main():
  async with Session() as session:
    story_id = randint(1, 10_000_000) # выбираем себе какой-нибудь красивый пост
    story = await session.get_story(story_id)

    print("Заголовок:", story.title)
    print("Оценки:", story.pluses, -story.minuses)
    print("Автор:", story.author.name)

    try:
      await session.auth('логин', 'пароль')
    except IncorrectLoginDetailsError:
      print('Неверный логин или пароль :(')
      return

    # await story.comment('Какой отличный пост!') <- вызовет ошибку (из-за плохого кода), так как был получен до авторизации

    # Получаем пост заново, чтобы оставить комментарий
    story = await session.get_story(story_id)

    # Оставляем комментарий
    await story.comment('Какой отличный пост!')

    # Смотрим комментарии поста
    async for comment in story.comments:
      print("Комментарий №" + str(comment.id))
      print(comment.author.name, 'написал "{}"'.format(comment.text))
      
      if comment.author.name == 'admin' or comment.is_user_pikabu_team:
        await comment.reply('Пишем что-то очень хорошее для лучших людей.')

if __name__ == "__main__":
  run(main())
```
