![](assets/logo.png)

# AnalyzerBot
### Телеграмм бот на основе pyrogram.

### Что делает:
- Собирает информацию о просмотрах на канале
- Сохраняет все данные в json файл
- Создает график активности за определенный промежуток времени

### Как настроить:
#### Установка:
```sh
git clone https://github.com/urancore/analyzerBotTg.git
```
```sh
cd analyzerBotTg
```
---
В **src\bot\config.py** укажите api/id hash и номер телефона.

В **src\bot\main.py**  укажите админа, ссылку на канал и лимит на количество постов.
```
pip install -r requirements.txt
```

```
python src\bot\main.py
```
