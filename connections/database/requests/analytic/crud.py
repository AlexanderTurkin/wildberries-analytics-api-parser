from connections.database import get_session


async def add_products(data_list):
    async for session in get_session():
        async with session.begin():
            session.add_all(data_list)
