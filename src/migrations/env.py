# ruff: noqa: E402
import sys
from pathlib import Path

current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent
sys.path.insert(0, str(src_dir))

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops

from src.config import settings
from src.database import BaseORM
from src.models import *  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseORM.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

writer = rewriter.Rewriter()


@writer.rewrites(ops.CreateTableOp)
def create_table_with_data(context, revision, op):
    if op.table_name == "access_levels":
        insert_op = ops.ExecuteSQLOp(
            """INSERT INTO access_levels (name) 
               VALUES ('User'), ('Premium'), ('Admin')
               ON CONFLICT (name) DO NOTHING"""
        )
        return [op, insert_op]
    if op.table_name == "data":
        insert_op = ops.ExecuteSQLOp(
            """INSERT INTO data (id, content, security_level) 
               VALUES (1, 'Общедоступная информация', 1), (2, 'Секретная информация', 2)
               ON CONFLICT DO NOTHING"""
        )
        return [op, insert_op]
    if op.table_name == "user_access_levels":
        insert_op = ops.ExecuteSQLOp(
            """INSERT INTO user_access_levels (id, user_id, access_level_id) 
               VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 1)
               ON CONFLICT DO NOTHING"""
        )
        return [op, insert_op]
    if op.table_name == "users":
        insert_op = ops.ExecuteSQLOp(
            """INSERT INTO users (id, first_name, last_name, email, hashed_password, is_active) 
               VALUES (1, 'ПОЛЬЗОВАТЕЛЬ', 'string', 'user@example.com', '$2b$12$EBtIRd7qO.cPyhtxF2r41.sGCl/.VQfti8geRnRK12imMSfOzG49O', true),
                      (2, 'АДМИН', 'string', 'user1@example.com', '$2b$12$licaRtyvApARaZqjt/NC3OiPmOjky9r5fkGQ8Otf/CrQoIroIlAke', true),
                      (3, 'ПРЕМИУМ', 'string', 'user2@example.com', '$2b$12$oziv7Dj/3m7IlT8v/EbP/ut0ETPA6YhgjLK1DxPLPLeidTvw6SKAK', true),
                      (4, 'ДЛЯ_УДАЛЕНИЯ', 'string', 'user3@example.com', '$2b$12$usamsN20LOHNknBP7A2CQuqulPLGF4cQOA4T/.ru3s7HCGeZ31CGq', true)
               ON CONFLICT DO NOTHING"""
        )
        return [op, insert_op]
    return op


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def after_create_table(target, connection, **kw):
        if target.name == "access_levels":
            connection.execute(
                """INSERT INTO access_levels (name) 
                   VALUES ('User'), ('Premium'), ('Admin')
                   ON CONFLICT (name) DO NOTHING"""
            )
        elif target.name == "data":
            connection.execute(
                """INSERT INTO data (id, content, security_level) 
                   VALUES (1, 'Общедоступная информация', 1), (2, 'Секретная информация', 2)
                   ON CONFLICT DO NOTHING"""
            )
        elif target.name == "user_access_levels":
            connection.execute(
                """INSERT INTO user_access_levels (id, user_id, access_level_id) 
                   VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 1)
                   ON CONFLICT DO NOTHING"""
            )
        elif target.name == "users":
            connection.execute(
                """INSERT INTO users (id, first_name, last_name, email, hashed_password, is_active) 
                   VALUES (1, 'ПОЛЬЗОВАТЕЛЬ', 'string', 'user@example.com', '$2b$12$EBtIRd7qO.cPyhtxF2r41.sGCl/.VQfti8geRnRK12imMSfOzG49O', true),
                          (2, 'АДМИН', 'string', 'user1@example.com', '$2b$12$licaRtyvApARaZqjt/NC3OiPmOjky9r5fkGQ8Otf/CrQoIroIlAke', true),
                          (3, 'ПРЕМИУМ', 'string', 'user2@example.com', '$2b$12$oziv7Dj/3m7IlT8v/EbP/ut0ETPA6YhgjLK1DxPLPLeidTvw6SKAK', true),
                          (4, 'ДЛЯ_УДАЛЕНИЯ', 'string', 'user3@example.com', '$2b$12$usamsN20LOHNknBP7A2CQuqulPLGF4cQOA4T/.ru3s7HCGeZ31CGq', true)
                   ON CONFLICT DO NOTHING"""
            )

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            after_create_table=after_create_table,
            process_revision_directives=writer,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
