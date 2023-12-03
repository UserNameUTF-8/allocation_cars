import datetime

from pydantic import BaseModel

"""
    ADMIN BASE MODELS
"""


class LoginBaseModel(BaseModel):
    email_admin: str
    password_admin: str


class ChangePasswordBaseModel(BaseModel):
    new_password: str


class SignUpBaseModel(LoginBaseModel):
    name_admin: str
    ip_admin: str | None = None


class AdminResponseBaseModel(SignUpBaseModel):
    id_admin: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_active: bool
    authority: int


class AdminUpdateBaseModel(BaseModel):
    id_admin: int | None = None
    name_admin: str | None = None
    ip_admin: str | None = None


class AdminUpdatePasswordBaseModel(BaseModel):
    id_admin: int
    password_admin: str


"""
    END ADMIN BASE MODELS
"""

"""
    USER BASE MODEL
"""


class AddUserBaseModel(BaseModel):
    name_user: str
    password_user: str
    email_user: str
    ip_user: str | None = None


class UserResponseBaseModel(AddUserBaseModel):
    id_user: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_active: bool
    points: int
    is_banned: bool


class UserUpdateBaseModel(BaseModel):
    id_user: int
    points: int | None = None
    is_banned: bool | None = None
    name_user: str | None = None


class UserPasswordModel(BaseModel):
    id_user: int
    new_password: str


"""
    END USER BASE MODEL
"""

"""
    HISTORY BASE MODEL
"""


class AddHistoryBaseModel(BaseModel):
    id_user: int
    id_car: int
    ret_date: datetime.datetime
    get_time: datetime.datetime | None = None
    price: float


class RetHistoryBaseModel(AddHistoryBaseModel):
    is_active: bool
    is_ok: bool
    is_dup: bool | None = None


"""
    END HISTORY BASEMODEL
"""

"""
    CAR BASEMODEL
"""


class AddCarBaseModel(BaseModel):
    identifyer_car: str
    color_car: str
    price_k_dinar: float
    model: str

    model_config = {
        "new_car_ex": {
            "identifyer_car": "BMW01",
            "color_car": "Black",
            "price_k_dinar": 2000.2,
            "model": "modelBMW01"
        }
    }


class CarResponseBaseModel(AddCarBaseModel):
    id_car: int
    is_active_car: int
    is_allocated_car: int
    is_mapped_car: int


class CarUpdateBaseModel(BaseModel):
    id_car: int
    car_color: str | None = None
    price_k_dinar: float | None = None


"""
    END CAR BASEMODEL
"""


class Details(BaseModel):
    detail: str


class AllocationBaseModel(BaseModel):
    """
    user_id
    car_id
    getdate
    price_
    ret_date
    is_active
    is_dup
    """
    id_history: int | None = None
    is_active: bool | None = None
    id_car: int
    id_user: int
    ret_date: datetime.datetime
    price_: float
    get_date: datetime.datetime | None = None
    is_dup: bool | None = None


class AllocationResponseBaseModel(AllocationBaseModel):
    id_history: int


class AllocationUpdateBaseModel(BaseModel):
    """
    user_id
    car_id
    getdate
    price_
    ret_date
    is_active
    is_dup
    """
    user_id: int
    car_id: int
    getdate: datetime.datetime
    price_: float | None = None
    ret_date: datetime.datetime | None = None
    is_active: bool | None = None
    is_dup: int | None = None


class NumbersResBaseModel(BaseModel):
    number_cars: int
    number_admins: int
    number_users: int
