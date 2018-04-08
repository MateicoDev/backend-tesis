import os


class DBSettings:
    SQLALCHEMY_DATABASE_URI = os.getenv("CLEARDB_DATABASE_URL", "").replace("?reconnect=true", "")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False