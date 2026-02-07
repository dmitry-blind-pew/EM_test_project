from src.repositories.access import AccessRepository
from src.repositories.admin import AdminRepository
from src.repositories.auth import UsersRepository
from src.repositories.data import DataRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.admin = AdminRepository(self.session)
        self.data = DataRepository(self.session)
        self.access = AccessRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
