import os
import sys

from config.command_line import CommandLine
from config.exec_parameters import ExecParameters
from dotenv import load_dotenv
from entrypoint.api_server import run_api_server
from entrypoint.crawler import Crawler
from infrastructure.log import Log

load_dotenv(dotenv_path=".env", override=True)
load_dotenv(dotenv_path=".env.secrets_and_paths", override=True)


def __initialize_log_and_db(verbose: bool = False):
    Log(verbose)
    Log.info("Starting")
    Log.info("Log initialized, verbose log at debug.log")

    if "OPENAI_API_KEY" not in os.environ:
        Log.error("Error: OPENAI_API_KEY env var is required")
        exit(-1)

    if "INPUT_SOURCE_PATH" not in os.environ:
        Log.error("Error: INPUT_SOURCE_PATH env var is required")
        exit(-1)

if __name__ == "__main__":
    is_api_server = "--api-server" in sys.argv

    # pre parse args to check if theres errors or to show help
    args = None
    if not is_api_server:
        args = CommandLine.parse_args()

    __initialize_log_and_db("--verbose" in sys.argv)

    if is_api_server:
        Log.info("Starting API server, other parameters are ignored")
        run_api_server()
    else:
        # execute as command line
        exec_params = ExecParameters.build_for_command_line(args)
        if len(exec_params.validate()) > 0:
            Log.error("Run with --help to check options")
            exit(-1)

        crawler = Crawler()
        crawler.execute()
