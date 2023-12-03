from database.MainDB import session
from sqlalchemy import select, func, update, Column, delete, and_
from database.DatabaseModels import Car
from sqlalchemy.exc import IntegrityError

from BaseModels import CarUpdateBaseModel, CarResponseBaseModel, AddCarBaseModel, Details


class ArgumentError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class IdentifierFound(RuntimeError):
    def __init__(self, message='Duplicate Identifier'):
        self.message = message
        super().__init__(message)


class IdentifierNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class CarRP:
    """
        ADD CAR, GET CAR BY IDENTIFIER, GET ALL CARS, GET ALL ACTIVE CAR
    """

    @staticmethod
    def dataValidation(car: AddCarBaseModel):
        if not 3 < len(car.identifyer_car) < 20:
            raise ArgumentError('Invalid Identifier')

        if not 2 < len(car.color_car) < 20:
            raise ArgumentError('Invalid Color')

        if not 2 < len(car.model) < 20:
            raise ArgumentError('Invalid Model')

    @staticmethod
    def addCar(new_car: AddCarBaseModel):
        """
        :raise IdentifierFound
        :param new_car:
        :return:
        """
        CarRP.dataValidation(new_car)
        car = CarRP.getByIdentifier(new_car.identifyer_car)

        if car is not None:
            raise IdentifierFound(f'car with identifier {new_car.identifyer_car} exists')

        isError = False
        new_car_ = Car(**new_car.__dict__)
        session.add(new_car_)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Car Exists")

        return CarRP.getCarByIdentifier(new_car.identifyer_car)

    @staticmethod
    def getCarByIdentifier(identity: str):
        if not 3 < len(identity) < 20:
            raise ArgumentError(f'Invalid Identifier')

        car_ = session.query(Car).filter(Car.identifyer_car == identity).first()

        if car_ is None:
            raise IdentifierNotFoundError

        return CarResponseBaseModel(**car_.__dict__)

    @staticmethod
    def getByIdentifier(id_: str):
        return session.query(Car).filter(Car.identifyer_car == id_).first()

    @staticmethod
    def getAllCars():
        active_cars = session.query(Car).all()

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, active_cars))
        return list_

    @staticmethod
    def updateCar(car_model_to_update: CarUpdateBaseModel):
        if car_model_to_update.car_color is None and car_model_to_update.price_k_dinar is None:
            raise ArgumentError('There is No Argument to Update')

        # query = update.where(Car.id_car == car_model_to_update.id_car)
        query = update(Car).where(Car.id_car == car_model_to_update.id_car)

        if car_model_to_update.car_color is not None:
            query = query.values({Car.color_car: car_model_to_update.car_color})

        if car_model_to_update.price_k_dinar is not None:
            query = query.values({Car.price_k_dinar: car_model_to_update.price_k_dinar})

        isError = False

        with session as s:
            s.execute(query)
            try:
                s.commit()
            except IntegrityError:
                s.rollback()
                isError = True

            if isError:
                raise ArgumentError('There is In Data You Provide')

        return CarResponseBaseModel(
            **session.query(Car).filter(Car.id_car == car_model_to_update.id_car).first().__dict__)

    @staticmethod
    def getAllActiveCars():

        active_cars = session.query(Car).filter(Car.is_active_car == 1).all()

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, active_cars))
        return list_

    @staticmethod
    def getAllAvailableCars():
        active_cars = session.query(Car).filter(Car.is_allocated_car == 0).filter(Car.is_active_car).all()

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, active_cars))

        return list_

    @staticmethod
    def getAvailableCarsWithColor(color: str):
        activeCarWithColor = session.query(Car).filter(
            and_(Car.color_car == color, Car.is_active_car == 1, Car.is_allocated_car == 0)).all()

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, activeCarWithColor))
        return list_

    @staticmethod
    def getAvailableCarWithModel(model: str):
        modelCarAvailable = session.query(Car).filter(
            Car.model == model).filter(Car.is_active_car == 1).filter(Car.is_allocated_car == 0).all()

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, modelCarAvailable))
        return list_

    @staticmethod
    def reActive(id_: int | str):
        statement = update(Car)

        if type(id_) is int:
            statement = statement.filter(Car.id_car == id_)
        else:
            statement = statement.filter(Car.identifyer_car == id_)
        print(str(statement).center(100, '-'))

        statement = statement.values({Car.is_active_car: True})

        print(str(statement).center(100, '-'))
        session.execute(statement)
        isError = False
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Update Failed")
        return {"detail": "Car Updated"}

    @staticmethod
    def getAvailableCarWithModelWithColor(model: str, color: str):
        modelCarAvailableWithModel = (session.query(Car).filter(Car.model == model).
                                      filter(Car.is_allocated_car == 0).
                                      filter(Car.is_active_car == 1).filter(Car.color_car == color)
                                      .all())

        def map_(car: Car):
            return CarResponseBaseModel(**car.__dict__)

        list_ = list(map(map_, modelCarAvailableWithModel))
        return list_

    @staticmethod
    def disActive(id_: int | str):
        statement = update(Car)
        if type(id_) is int:
            statement = statement.where(Car.id_car == id_)
        else:
            statement = statement.where(Car.identifyer_car == id_)

        statement = statement.values({Car.is_active_car: False})
        session.execute(statement)
        isError = False
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Update Failed")
        return {"details": "Car DisActive"}

    @staticmethod
    def allocate(id_: int):
        statement = update(Car).where(Car.id_car == id_).values({Car.is_allocated_car: True})
        session.execute(statement)
        isError = False
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Allocation Failed")
        return True

    @staticmethod
    def diAllocate(id_: int):
        statement = update(Car).where(Car.id_car == id_).values({Car.is_allocated_car: False})
        session.execute(statement)
        isError = False
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Car Exists")
        return True

    @staticmethod
    def allocateByIdentifier(identifier: str):
        statement = update(Car).where(Car.identifyer_car == identifier).values({Car.is_allocated_car: True})
        session.execute(statement)
        isError = False
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            isError = True

        if isError:
            raise ArgumentError("Car Exists")
        return {"details": f"Car with identifier {identifier} allocated"}

    @staticmethod
    def deleteCar(id_: int | str):
        statement = delete(Car)
        if type(id_) is int:
            statement = statement.where(Car.id_car == id_)
        else:
            statement = statement.where(Car.identifyer_car == id_)

        session.execute(statement)
        session.commit()
        return {"detail": f"Car with identifier {id_} deleted"}

    @staticmethod
    def getCarById(id_: int):
        car = session.query(Car).filter(Car.id_car == id_).first()
        if car is None:
            raise IdentifierNotFoundError
        return CarResponseBaseModel(**car.__dict__)

    @staticmethod
    def getNumberCars():
        query = select(func.count()).select_from(Car)
        return session.execute(query).first()[0]

    @staticmethod
    def getModelsAvailable():
        list_models = session.query(Car.model).distinct().all()

        def transformToString(item: Column[str]):
            return item[0]

        rest = list(map(transformToString, list_models))
        return rest


if __name__ == '__main__':
    new_car = AddCarBaseModel(identifyer_car='car002', model='BMW03', color_car='black', price_k_dinar=20003)
    CarRP.addCar(new_car)
    # CarRP.disActive('car002')
    print(CarRP.getModelsAvailable())
    # CarRP.addCar(new_car)
