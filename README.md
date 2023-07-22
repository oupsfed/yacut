1. О чем проект:

Проект YaCut — это сервис укорачивания ссылок. 
Его назначение — ассоциировать длинную пользовательскую 
ссылку с короткой, которую предлагает сам 
пользователь или предоставляет сервис.

2. Стек:

- flask 2.0.2
- sqlalchemy 1.4.29
- jinja2 3.0.3

3. Автор:

Никита Федоров (github: https://github.com/oupsfed)

4. Как запустить локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:oupsfed/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
