import uvicorn
from fastapi import FastAPI

from controllers.AdminController import adminRouter
from controllers.AllocationController import allocationRouter
from controllers.UserController import userRouter
from controllers.CarController import carRoute

app = FastAPI()


@app.get("/")
def home():
    return "It Work"


app.include_router(adminRouter, tags=['Admins'])
app.include_router(userRouter, tags=['Users'])
app.include_router(carRoute, tags=['Car'])
app.include_router(allocationRouter, tags=['History'])

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')
