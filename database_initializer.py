import aiosqlite
from os import getenv
from dotenv import load_dotenv


database_name = "history_database.sqlite"
default_history = {
        "internal": [
            [
                "<|BEGIN-VISIBLE-CHAT|>",
                "Greetings! I am Ralsei! You, it's wonderful to meet you!"
            ]
        ],
        "visible": [
            [
                "",
                "Greetings! I am Ralsei! You, it's wonderful to meet you!"
            ]
        ]
    }


async def create_database():
    async with aiosqlite.connect(database_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
                id        INTEGER           not null
                    primary key,
                is_banned INTEGER default 0 not null
            )
        ''')
        await db.execute(f'''
            CREATE TABLE IF NOT EXISTS history
            (
                id   INTEGER not null
                    primary key
                    references users
                        on delete cascade,
                data TEXT    not null default ({default_history})
            )
        ''')
        await db.commit()
