from typing import List, Optional
from models.users import User, UserIn
from .base import BaseRepository
from db.users import users
from core.security import hash_password, verify_passowrd
import datetime

class UserReposiory(BaseRepository):
    async def get_all(self, limit: int=100, skip: int=0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query) 

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id==id).first()
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> List[User]:
        user = User(
            name=u.name,
            email=u.email,
            hashed_passowrd=hash_password(u.password),
            is_company=u.is_company,
            created_date=datetime.datetime.utcnow(),
            updated_date=datetime.datetime.utcnow()
        )

        values = {**user.dict}
        values.pop("id", None)

        query = users.insert().values()
        user.id = await self.database.execute(query)
        return user

    async def update(self, u: UserIn) -> List[User]:
        user = User(
            id=id, 
            name=u.name,
            email=u.email,
            hashed_passowrd=hash_password(u.password),
            is_company=u.is_company,
            created_date=datetime.datetime.utcnow(),
            updated_date=datetime.datetime.utcnow()
        )

        values = {**user.dict}
        values.pop("created_date", None)
        values.pop("id", None)

        query = users.update().where(users.c.id==id).values()
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> List[User]:
        query = users.select().where(users.c.email==email).first()
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)
