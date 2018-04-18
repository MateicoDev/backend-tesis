import os


class DBSettings:
    SQLALCHEMY_DATABASE_URI = "postgres://jwbagcrhzmjmsx:9dd6877b1798bd19068f51634f185bf2" \
                              "faeea252b0c03aa63adc15959c25a2ff@ec2-54-83-204-6.compute-1." \
                              "amazonaws.com:5432/d51b6ojme45csq"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DB_ENGINE = "postgresql"
    DB_HOST = "localhost"
    DB_NAME = os.getenv("DB_NAME", "d51b6ojme45csq")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")