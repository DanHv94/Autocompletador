import os

import uvicorn
import typer
from fastapi import FastAPI, Request, status

from application import create_app

command_app = typer.Typer(add_completion=False)
app = create_app()

@app.get("/api")
async def index():
    return {"response": "OK"}

@command_app.command()
def run():
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)

if __name__ == "__main__":
    command_app()