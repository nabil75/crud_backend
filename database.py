import asyncpg

db_params = {
        'database': 'quaeroquesto',
        'user': 'postgres',
        'password': 'nBl030130!',
        'host': 'localhost',
        'port': '5432',
    }

async def postgres_select_query(query, *params):
        conn = await asyncpg.connect(**db_params)
        values = await conn.fetch(query, *params)
        await conn.close()
        return values   

async def postgres_insert_query(query, *params):
        conn = await asyncpg.connect(**db_params)
        last_id = await conn.fetchval(query, *params)
        await conn.close()
        return last_id


async def postgres_update_query(query, *params):
        conn = await asyncpg.connect(**db_params)
        await conn.execute(query, *params)
        await conn.close()
        return "Update query executed successfully."


async def postgres_delete_query(query, *params):
        conn = await asyncpg.connect(**db_params)
        await conn.execute(query, *params)
        await conn.close()
        return "Delete query executed successfully."

