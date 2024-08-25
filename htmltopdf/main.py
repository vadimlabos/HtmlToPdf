import uvicorn
import argparse

from fastapi import FastAPI
from htmltopdf.routers import convert, health
from htmltopdf.utils.utils import Utils

app = FastAPI()
app.include_router(convert.router)
app.include_router(health.router)

if __name__ == "__main__":
    args = Utils.parse_arguments()

    if not args.debug:
        '''
        Workers On, Reload Off
        '''
        uvicorn.run("main:app",
                    host=Utils.get_settings().address,
                    port=Utils.get_settings().port,
                    timeout_keep_alive=Utils.get_settings().timeout_keep_alive_sec,
                    log_level=Utils.get_settings().log_level,
                    use_colors=True,
                    workers=Utils.get_settings().workers)
    else:
        '''
        Reload On, workers Off
        '''
        uvicorn.run("main:app",
                    host=Utils.get_settings().address,
                    port=Utils.get_settings().port,
                    timeout_keep_alive=Utils.get_settings().timeout_keep_alive_sec,
                    log_level=Utils.get_settings().log_level,
                    use_colors=True,
                    reload=True)
