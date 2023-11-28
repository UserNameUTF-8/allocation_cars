from database.MainDB import session
from sqlalchemy import Update, Delete, select, func
from Utils import sha256
from database.DatabaseModels import User
from sqlalchemy.exc import IntegrityError
from BaseModels import AddUserBaseModel, UserResponseBaseModel, UserUpdateBaseModel, UserPasswordModel, Details


class ArgumentError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class MailExistsError(RuntimeError):
    def __init__(self, message='Mail Exists Error'):
        self.message = message
        super().__init__(message)


class UserNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UserRP:
    @staticmethod
    def dataValidation(user: AddUserBaseModel):
        if len(user.email_user) < 4 or not user.email_user.__contains__('@') or len(user.email_user) > 100:
            raise ArgumentError('Email Invalid')

        if len(user.password_user) < 7:
            raise ArgumentError('Password Too Short')

        if user.ip_user is not None:
            if not 8 < len(user.ip_user) < 32:
                raise ArgumentError('Invalid IP Address')

        if not 4 < len(user.name_user) < 100:
            raise ArgumentError("Invalid Name")

    @staticmethod
    def addUser(user: AddUserBaseModel) -> UserResponseBaseModel:

        """
        :raise MailExistsError
        :param user:
        :return: UserResponseBaseModel
        """
        UserRP.dataValidation(user)
        user.password_user = sha256(user.password_user)
        user_ = User(**user.__dict__)
        session.add(user_)
        try:
            session.commit()
        except IntegrityError:
            raise MailExistsError

        return UserRP.getUserByEmail(user.email_user)

    @staticmethod
    def getUserByEmail(email: str) -> UserResponseBaseModel:
        """
        :raise UserNotFoundError
        :param email:
        :return UserResponse:
        """
        user = session.query(User).filter(User.email_user == email).first()
        if user is None:
            raise UserNotFoundError(f'User with email {email} Not Found')

        return UserResponseBaseModel(**user.__dict__)

    @staticmethod
    def getUserById(id_: int) -> UserResponseBaseModel:
        """
        :raise UserNotFoundError
        :param id_:
        :return UserResponseBaseModel:
        """

        user = session.query(User).filter(User.id_user == id_).first()

        if user is None:
            raise UserNotFoundError(f'user with id {id_} does not Exists')

        return UserResponseBaseModel(**user.__dict__)

    @staticmethod
    def getAllUsers() -> list[UserResponseBaseModel]:
        """
        :return list[UserResponseBaseModel]:
        """

        users_ = session.query(User).all()

        def map_(user: User):
            return UserResponseBaseModel(**user.__dict__)

        new_list = list(map(map_, users_))
        return new_list

    @staticmethod
    def getAllActiveUsers() -> list[UserResponseBaseModel]:
        active_users = session.query(User).filter(User.is_active).all()

        def map_(user: User):
            return UserResponseBaseModel(**user.__dict__)

        new_list = list(map(map_, active_users))
        return new_list

    @staticmethod
    def getAllBannedUsers() -> list[UserResponseBaseModel]:
        banned_users = session.query(User).filter(User.is_banned).all()

        def map_(user: User):
            return UserResponseBaseModel(**user.__dict__)

        new_list = list(map(map_, banned_users))
        return new_list

    @staticmethod
    def getUsersByName(name: str) -> list[UserResponseBaseModel]:
        users_ = session.query(User).filter(User.name_user == name).all()

        def map_(user: User):
            return UserResponseBaseModel(**user.__dict__)

        new_list = list(map(map_, users_))
        return new_list

    @staticmethod
    def searchUsersByName(keyword: str) -> list[UserResponseBaseModel]:
        users_ = session.query(User).filter(User.name_user.like(f'%{keyword}%'))

        def map_(user: User):
            return UserResponseBaseModel(**user.__dict__)

        new_list = list(map(map_, users_))
        return new_list

    @staticmethod
    def updatedUser(userToUpdate: UserUpdateBaseModel) -> UserResponseBaseModel:
        """
        :raise ArgumentError
        :param userToUpdate:
        :return:
        """

        is_updated = False
        query_ = Update(User).where(userToUpdate.id_user == User.id_user)
        if userToUpdate.name_user:
            if not 4 < len(userToUpdate.name_user) < 100:
                raise ArgumentError('Invalid User')

            query_ = query_.values({User.name_user: userToUpdate.name_user})
            is_updated = True

        if userToUpdate.points:
            if not 0 < userToUpdate.points < 200:
                raise ArgumentError('Point Out Of Range')
            query_ = query_.values({User.points: userToUpdate.points})
            is_updated = True

        if not is_updated:
            ArgumentError('No Fields to Update')

        session.execute(query_)
        session.commit()

        user_ = UserRP.getUserById(userToUpdate.id_user)
        return user_

    @staticmethod
    def banneUser(id_: int):
        query = Update(User).where(User.id_user == id_)
        query = query.values({User.is_banned: True})
        session.execute(query)
        session.commit()
        return session.query(User).filter(User.id_user == id_).first()

    @staticmethod
    def unBanneUser(id_: int):
        query = Update(User).where(User.id_user == id_)
        query = query.values({User.is_banned: False})
        session.execute(query)
        session.commit()
        return session.query(User).filter(User.id_user == id_).first()

    @staticmethod
    def disActiveUser(id_: int):
        query = Update(User).where(User.id_user == id_)
        query = query.values({User.is_active: 0})
        session.execute(query)
        session.commit()
        return session.query(User).filter(User.id_user == id_).first()

    @staticmethod
    def active(id_: int):
        query = Update(User).where(User.id_user == id_)
        query = query.values({User.is_active: 1})
        session.execute(query)
        session.commit()
        return session.query(User).filter(User.id_user == id_).first()

    @staticmethod
    def updatePassword(userPass: UserPasswordModel):
        query = Update(User).where(User.id_user == userPass.id_user).values(
            {User.password_user: sha256(userPass.new_password)})
        session.execute(query)
        session.commit()
        return UserRP.getUserById(userPass.id_user)

    @staticmethod
    def deleteUser(id_: int) -> Details:
        query = Delete(User).where(User.id_user == id_)
        UserRP.getUserById(id_)  # Error Generator
        session.execute(query)
        session.commit()

        return Details(detail="User Deleted")

    @staticmethod
    def numberOfUsers():
        query = select(func.count()).select_from(User)
        return session.execute(query).first()[0]


if __name__ == '__main__':
    # users = UserRP.getAllUsers()
    # new_user = UserRP.addUser(
    #     AddUserBaseModel(name_user='User01', password_user='password_1', email_user='user01@go.com'))
    # users1 = UserRP.getAllUsers()
    # print(users1)
    print(UserRP.numberOfUsers())
