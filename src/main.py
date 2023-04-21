""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["FusionSid"]
__licence__ = "MIT License"

import os
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


@app.on_event("shutdown")
async def shutdown_event():
    print("[bold blue]API has been shutdown!")
    # cleanup tasks if needed


for route in router_list:
    app.include_router(router=route)

for middleware in middleware_list:
    app.add_middleware(middleware)

register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)

PORT = 8443
SSL_CERTFILE_PATH = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH = join(dirname(__file__), "key.pem")
both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])

devmode = os.environ.get("DEVMODE", "").lower()
if devmode not in ["true", "false"]:
    raise InvalidDevmodeValue(provided=devmode)

if devmode == "true" or not both_certfiles_exist:
    options = {"app": "main:app", "port": PORT, "reload": True}
else:
    options = {
        "app": "main:app",
        "reload": False,
        "port": PORT,
        "access_log": False,
        "ssl_keyfile": SSL_KEYFILE_PATH,
        "ssl_certfile": SSL_CERTFILE_PATH,
    }


if __name__ == "__main__":
    uvicorn.run(**options)
