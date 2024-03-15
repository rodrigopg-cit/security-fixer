import os
import traceback

from config.exec_parameters import ExecParameters
from entrypoint.crawler import Crawler
from entrypoint.dto.generate_base_dto import GenerateBaseDto
from infrastructure.log import Log

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from uvicorn import run as uvicorn_run


class ResponseModel(BaseModel):
    success: bool = True


class ResponseErrorModel(BaseModel):
    error: str = ""


middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin()
        )
    )
]


app = FastAPI(debug=True,
              title='Security Fixer',
              description='Correção de vulnerabilidades de segurança a partir de código fonte existente',
              middleware=middleware)


@app.post(path="/security-fixer",
          summary="Aplica correções de vulnerabilidades de segurança",
          response_description="Retorna sucesso ou erro",
          response_model=ResponseModel,
          responses={500: {"description": "Internal Server Error", "model": ResponseErrorModel},
                     422: {"description": "Unprocessable Entity", "model": ResponseErrorModel},
                     400: {"description": "Bad Request", "model": ResponseErrorModel}})
def generate_business_rules(params: GenerateBaseDto):
    return __generate(params)



def __generate(params: GenerateBaseDto):
    try:
        exec_params = ExecParameters.build_for_api(params)
        msgs_error = exec_params.validate()
        if len(msgs_error):
            return JSONResponse(content={"error": "\n".join(msgs_error)}, status_code=400)
        crawler = Crawler()
        crawler.execute()
        return {"success": True}
    except Exception as e:
        stacktrace = traceback.format_exc()
        Log.error(f"Error: {e}\n{stacktrace}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


def run_api_server():
    uvicorn_options = {
        "app": "entrypoint.api_server:app",
        "host": os.environ["API_SERVER_HOST"],
        "port": int(os.environ["API_SERVER_PORT"]),
        "reload": os.environ["API_SERVER_RELOAD"] == "1",
        "reload_dirs": ["src"],
    }

    Log.info(f"Swagger at http://{uvicorn_options['host']}:{uvicorn_options['port']}/docs")

    uvicorn_run(**uvicorn_options)
