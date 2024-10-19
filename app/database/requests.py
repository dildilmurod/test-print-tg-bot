from app.database.models import async_session
from app.database.models import User, Category, Product
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category(category_id):
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id == category_id))


async def get_product(product_id):
    async with async_session() as session:
        return await session.scalar(select(Product).where(Product.id == product_id))


async def get_product_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Product).where(Product.category == category_id))
