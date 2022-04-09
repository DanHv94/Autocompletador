""" File that defines the creation and configuration of the FastAPI app.
"""
from logging.config import dictConfig
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette_context.middleware.context_middleware import ContextMiddleware


def create_app() -> FastAPI:
    """ Function that creates and configures the FastAPI app.

    Returns:
        app(FastAPI): Configured FastAPI app
    """
    logger_levels = {
        'dev': 'INFO',
        'staging': 'WARNING',
        'prod': 'ERROR'
    }

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters":  {
            'default': {
                "()": "uvicorn.logging.DefaultFormatter",
                "format": '%(levelprefix)s %(asctime)s - File %(filename)s, line %(lineno)s: %(message)s',
                "datefmt": "%d-%m-%Y %H:%M:%S"
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": logger_levels.get(os.getenv('ENV', 'dev'), 'INFO')
            },
        },
    }

    dictConfig(logger_config)

    middleware = [
        Middleware(
            ContextMiddleware,
        )
    ]

    # This imports are done here to make sure that the subsecuent logger are
    # loaded with the desired configuration
    from controllers import ( 
        citiesController
    )
    from config import (
        ENV
    )


    # FastAPI app
    debug = ENV == 'dev'
    app = FastAPI(
        debug=debug,
        version='1.0.0',
        middleware=middleware,
        docs_url=('/docs' if ENV != 'prod' else None),
        openapi_url='/openapi.json'
    )

    app.include_router(citiesController.router)

    '''app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )'''
    return app