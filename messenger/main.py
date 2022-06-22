from fastapi import FastAPI
import uvicorn

from endpoints.login import router as login_router
from endpoints.user import router as user_router
from endpoints.chat import router as chat_router
from endpoints.utils import router as utils_router
from endpoints.message import router as message_router
from core.db.session import engine
from core.db.models import Base

import subprocess
import atexit

app = FastAPI()

app.include_router(user_router, tags=["user"])
app.include_router(login_router, tags=["login"])
app.include_router(utils_router, tags=["utils"])
app.include_router(chat_router, tags=["chat"])
app.include_router(message_router, tags=["message"])


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    subprocess.Popen(['./run_celery.sh'])
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8080,
        reload=True,
        debug=True,
    )


def on_stop():
    print(">>>>>>>>>>>>>>>>> KILLING CELERY <<<<<<<<<<<<<<<<<<<")
    subprocess.Popen(['./kill_celery.sh'])


atexit.register(on_stop)