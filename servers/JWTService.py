import datetime

from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def createAccessToken(data: dict, expTime: datetime.datetime | None = None):
    data_to_encode = data.copy()

    if expTime is None:
        expTime = datetime.datetime.now() + datetime.timedelta(days=10)  # 10 days exp time

    data_to_encode.update({"exp": expTime})
    encoded_data = jwt.encode(data_to_encode, algorithm=ALGORITHM, key=SECRET_KEY)
    return encoded_data


def decodeAccessToken(token: str):
    data_ = jwt.decode(token, algorithms=ALGORITHM, key=SECRET_KEY)
    return data_
