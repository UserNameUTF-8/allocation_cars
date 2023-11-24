import unittest
from database.CarDB import Car
from database.AdminDB import Admin
from database.HistoryDB import History
from database.UserDB import User


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


class AdminDBTest(unittest.TestCase):
    def insertionAdminTest(self):
        self.assertEqual("Hello", "Hello")

    def updateAdminTest(self):
        pass

    def getAdminsTest(self):
        pass

    def deleteAdminTest(self):
        pass


class UserDBTest(unittest.TestCase):
    def insertionUserTest(self):
        pass

    def updateUserTest(self):
        pass

    def getUsersTest(self):
        pass

    def deleteUserTest(self):
        pass


class CarDBTest(unittest.TestCase):
    def insertionCarTest(self):
        pass

    def updateCarTest(self):
        pass

    def getCarsTest(self):
        pass

    def deleteCarTest(self):
        pass


class HistoryDBTest(unittest.TestCase):
    def insertionHistoryTest(self):
        pass

    def updateHistoryTest(self):
        pass

    def getHistoriesTest(self):
        pass

    def deleteHistoryTest(self):
        pass


if __name__ == '__main__':
    unittest.main()
