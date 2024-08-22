import uvicorn
from fastapi import FastAPI
from htmltopdf.routers import convert
from htmltopdf.utils.utils import Utils

app = FastAPI()
app.include_router(convert.router)


@app.get("/status")
async def healthcheck():
    return {"message": "Healthy"}

if __name__ == "__main__":
    # for manual run and debug
    uvicorn.run("main:app",
                host=Utils.get_settings().address,
                port=Utils.get_settings().port,
                timeout_keep_alive=Utils.get_settings().timeout_keep_alive_sec,
                log_level=Utils.get_settings().log_level,
                use_colors=True,
                workers=Utils.get_settings().workers)
