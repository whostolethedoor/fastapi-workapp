from fastapi import FastAPI
from db.base import database
from endpoints.users import router
import uvicorn


# app = FastAPI(title="employment exchange")
# app.include_router(router, prefix="/users", tags=['users']) 


def get_application() -> FastAPI:
    application = FastAPI(title="ggg")
    application.include_router(router, prefix='/users', tags=['users'])
    return application


app = get_application()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)