from database.DatabaseModels import History, Admin, Car, User
from database.MainDB import mainEngine

if __name__ == '__main__':
    History.__table__.drop(mainEngine)
    Car.__table__.drop(mainEngine)
    Admin.__table__.drop(mainEngine)
    User.__table__.drop(mainEngine)
    print('construct'.center(100, '-'))
    Car.__table__.create(mainEngine)
    Admin.__table__.create(mainEngine)
    User.__table__.create(mainEngine)
    History.__table__.create(mainEngine)
