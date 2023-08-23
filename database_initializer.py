import aiosqlite
from os import getenv
from dotenv import load_dotenv


database_name = "history_database.sqlite"


async def create_database():
    async with aiosqlite.connect(database_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
                id                INTEGER not null
                    primary key
                    ON DElETE CASCADE,
                is_banned INTEGER default (0) not null 
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS history
            (
                id INTEGER not null primary key references users,
                data TEXT not null
            )
        ''')
        await db.commit()
