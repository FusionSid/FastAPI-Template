""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["FusionSid"]
__licence__ = "MIT License"

import os
from typing import Final
from os.path import dirname, join, exists

import uvicorn
from rich import print
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

from routes import router_list, middleware_list
from core import TheAPI, TORTOISE_CONFIG, InvalidDevmodeValue

load_dotenv()
app = TheAPI(__version__)


@app.on_event("startup")
async def startup_event():
    print("[bold blue]API has started!")
    # run startup tasks for things eg redis connection


@app.on_event("shutdown")
async def shutdown_event():
    print("[bold blue]API has been shutdown!")
    # cleanup tasks if needed


# add all routers
for route in router_list:
    app.include_router(router=route)

# add all middleware
for middleware in middleware_list:
    app.add_middleware(middleware)

# connect to db through tortoise orm
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)

PORT: Final = 8443
SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")

# check that both certificate files exist
both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])

# check if to startup api in dev mode or not
devmode = os.environ.get("DEVMODE", "").lower()
if devmode not in ["true", "false"]:
    raise InvalidDevmodeValue(provided=devmode)

# set the uvicorn server options based one dev mode or not
options = (
    {"app": "main:app", "port": PORT, "reload": True}
    if devmode == "true" or not both_certfiles_exist
    else {
        "app": "main:app",
        "reload": False,
        "port": PORT,
        "access_log": False,
        "ssl_keyfile": SSL_KEYFILE_PATH,
        "ssl_certfile": SSL_CERTFILE_PATH,
    }
)


if __name__ == "__main__":
    uvicorn.run(**options)
