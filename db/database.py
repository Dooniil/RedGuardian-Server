import json
from os import getcwd, sep
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text, dialects


class DatabaseException(Exception):
    pass


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
        self._db_url = None
        self.__conn_info = None

        self.__base = declarative_base()

    @property
    def metadata(self):
        return self.__base.metadata

    @property
    def base(self):
        return self.__base

    @property
    def conn_info(self):
        if not self.__conn_info:
            self.__get_conn_info()

        return self.__conn_info['db_user'], self.__conn_info['db_pass'], self.__conn_info['db_host'], \
            self.__conn_info['db_port'], self.__conn_info['db_name']

    @conn_info.setter
    def conn_info(self, dict_):
        self.__conn_info = dict_

    def __getattr__(self, name):
        return getattr(self._session, name)

    def __get_conn_info(self) -> None:
        path = sep.join([getcwd(), 'db', 'db_config.json'])
        try:
            with open(path, 'r') as file:
                self.conn_info = json.loads(file.read())
        except Exception as e:
            raise DatabaseException(f'Ошибка при чтении конфигурационного файла:\nСообщение: {e.args}')

    async def check_connection(self) -> None:
        try:
            await self.execute(text('SELECT 1'))
        except ConnectionRefusedError:
            raise DatabaseException('Connection to DB has been failed... \nRestart program')

    async def init(self):
        self.__get_conn_info()
        user, password, host, port, name = self.conn_info
        self._db_url = f"postgresql+asyncpg://{user}:{password}@" \
                       f"{host}:{port}/{name}"
        self._engine = create_async_engine(self._db_url, echo=True)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def check_scructure(self):
        dialect = dialects.postgresql.dialect()
        tables = self.metadata.tables
        correct_table_list = [
            tables['credential'],
            tables['scanner'], 
            tables['host'],
            tables['group_hosts'],
            tables['GroupsHosts'],
            tables['task'],
            tables['json_definition'],
            tables['execute_definition'],
            tables['task_result'],
            tables['scan_result']
            ]
        for table in correct_table_list:
            schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
            query = str(schema.compile(dialect=dialect))
            await self.execute(text(query))
            await self.commit()


async_db_session = AsyncDatabaseSession()
