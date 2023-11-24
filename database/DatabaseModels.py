import datetime
from sqlalchemy import Column, String, Boolean, Integer, Double, ForeignKey, DateTime, TEXT
from sqlalchemy.orm import relationship
from database.MainDB import Base


class Car(Base):
    __tablename__ = 'cars'
    id_car = Column(Integer, primary_key=True, autoincrement=True)
    identifyer_car = Column(String(20), unique=True, nullable=False)
    color_car = Column(String(40))
    price_k_dinar = Column(Double, nullable=False)
    is_active_car = Column(Boolean, default=True)
    is_allocated_car = Column(Boolean, default=False)
    is_mapped_car = Column(Boolean, default=False)
    model = Column(String(100), nullable=False)
    car_allocation_history = relationship("History", back_populates='car_')

    def __init__(self, identifyer_car: str, model: str, color_car: str, price_k_dinar: float):
        """
        :param identifyer_car:
        :param model:
        :param color_car:
        :param price_k_dinar:
        """
        self.identifyer_car = identifyer_car
        self.color_car = color_car,
        self.price_k_dinar = price_k_dinar
        self.model = model


class Admin(Base):
    __tablename__ = 'admins'
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    name_admin = Column(String(100), nullable=False)
    ip_admin = Column(String(100))
    password_admin = Column(TEXT, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    email_admin = Column(String(200), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    authority = Column(Integer, default=2)

    def __init__(self, name_admin: str, password_admin: str, email_admin: str, ip_admin: str | None = None):
        """
        :param name_admin:
        :param password_admin:
        :param email_admin:
        :param ip_admin: optional
        """
        self.name_admin = name_admin
        self.password_admin = password_admin
        self.email_admin = email_admin
        self.ip_admin = ip_admin


class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name_user = Column(String(100), nullable=False)
    ip_user = Column(String(100))
    password_user = Column(TEXT, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    email_user = Column(String(200), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    points = Column(Integer, default=100)
    is_banned = Column(Boolean, default=False)
    allocation_history = relationship("History", back_populates='user_')

    def __init__(self, name_user: str, password_user: str, email_user: str, ip_user: str | None = None):
        self.name_user = name_user
        self.password_user = password_user
        self.email_user = email_user
        self.ip_user = ip_user

    def __repr__(self):
        return f'User(id={self.id_user}, email={self.email_user})'


class History(Base):
    __tablename__ = 'history'
    id_history = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    id_car = Column(Integer, ForeignKey('cars.id_car'), nullable=False)
    get_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    ret_date = Column(DateTime, nullable=False)
    price_ = Column(Double, nullable=False)
    is_ok = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    is_dup = Column(Boolean, nullable=True, default=False)
    user_ = relationship("User", back_populates='allocation_history')
    car_ = relationship("Car", back_populates='car_allocation_history')

    def __init__(self, id_user, id_car, ret_date, price_, getdate: datetime.datetime | None = None,
                 is_dup: bool | None = None):
        self.id_car = id_car
        self.id_user = id_user
        self.ret_date = ret_date
        self.price_ = price_
        self.is_dup = is_dup

        if getdate is not None:
            self.get_date = getdate

    def __repr__(self):
        return f'User : {self.id_user} Car: {self.id_car}'


if __name__ == '__main__':
    # car = Car('192 TN 1202', 'bmw13', 'black', 10000.2)
    # session.add(car)

    # user = User('user1', 'password', 'email@go.com')
    # session.add(user)
    History.__table__.drop()
    History.__table__.create()
