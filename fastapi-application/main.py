from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from api import router as api_router
from api_v1 import router as router_api_v1
from core.config import settings
from core.models import db_helper, Base


# as soon as app is async use async manager to specify actions
# which gonna happen on app start and shoutdown
@asynccontextmanager
async def lifespan(app:FastAPI):
    # here is actions happen on startup
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Dispose engine")
    await db_helper.dispose()
    # Clean up and release resources on shutdown



app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
from api_v1.users import router as user_router
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
    # Will watch for changes in these directories
    # create automatic reload with saving files,
    # show path to file and fast API object to reload

