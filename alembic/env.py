from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. IMPORT YOUR APP BASE & SETTINGS HERE
from app.database import Base
from app.config import settings
import app.models  # Ensures models are registered with Base

# 2. THIS IS THE ALEMBIC CONFIG OBJECT
config = context.config

# 3. OVERWRITE THE SQLALCHEMY URL WITH YOUR SETTINGS
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. SET TARGET METADATA
target_metadata = Base.metadata