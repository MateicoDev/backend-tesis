import os


class DBSettings:
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://jwbagcrhzmjmsx:9dd6877b1798bd19068f51634f185bf2" \
    #                           "faeea252b0c03aa63adc15959c25a2ff@ec2-54-83-204-6.compute-1." \
    #                           "amazonaws.com:5432/d51b6ojme45csq"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DB_ENGINE = "postgresql+psycopg2"
    DB_HOST = os.getenv("RDS_HOSTNAME", "ec2-54-83-204-6.compute-1.amazonaws.com")
    DB_NAME = os.getenv("DB_NAME", "d85margr3hj353")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USERNAME", "muuaqgzvffjhmq")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "26a798f2f87dfcc9a3c84de6f1e908b6e5eaf7b34bf25b98de093029cda1149b")
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}:{4}/{5}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT,
                                                                 DB_NAME)

