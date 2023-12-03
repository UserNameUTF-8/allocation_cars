import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME_')
PASSWORD = os.getenv('PASSWORD')
HOSTNAME = os.getenv('HOSTNAME')
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')

# mainEngine = create_engine(url=f'mysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}', echo=True)
mainEngine = create_engine(
    f"mysql://{USERNAME}:{PASSWORD}@mysql-1ab537cc-essid101010-3c12.a.aivencloud.com:21800/defaultdb", echo=True)
Session = sessionmaker(mainEngine)
session = Session()
Base = declarative_base()

if __name__ == '__main__':
    Base.metadata.create_all(mainEngine)
    print(mainEngine)
