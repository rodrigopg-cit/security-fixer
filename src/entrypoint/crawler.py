import logging
import os
import time
import traceback
from datetime import timedelta

from config.exec_parameters import ExecParameters
from infrastructure.chat import ChatClient, ChatClientParams
from infrastructure.log import Log
from template.fixer_42crunch_template import Fixer42CrunchTemplate


class Crawler():
    def execute(self):
        ChatClient().reset_usage()

        start_time = time.monotonic()

        exec_params = ExecParameters.instance()

        Log.info(f"""Entrypoint Folder: {exec_params.entrypoint_folder}
         Security Tool: {exec_params.security_tool}""")

        self.__security_fixer(exec_params)

        self.__print_summary()

        end_time = time.monotonic()
        Log.info(f"Finished: {timedelta(seconds=end_time - start_time)}")

    def __security_fixer(self, exec_params: ExecParameters):
        Log.info("Crawling files to fix security vulnerabilities")
        self.__crawl_folder(
            entrypoint_folder=exec_params.entrypoint_folder,
            security_tool=exec_params.security_tool
        )
        Log.info("Finished crawling files to fix security vulnerabilities")


    @classmethod
    def __print_summary(cls):
        Log.info("############# SUMMARY #############")
        Log.info(f"Tokens Chat total input : {ChatClient().input_tokens_used()}")
        Log.info(f"Tokens Chat total output: {ChatClient().output_tokens_used()}")
        Log.info(f"Tokens Chat total       : {ChatClient().tokens_used()}")
        Log.info(f"Total  Chat (USD)       : ${format(ChatClient().total_cost(), '.4f')}")
        Log.info("###################################")

    def __crawl_folder(self,
                        entrypoint_folder: str,
                        security_tool: str):

        directory_path = os.path.join(ExecParameters.instance().input_source_path, entrypoint_folder)

        # Walk through all directories and files in the directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                try:
                    # Open and read the content of the file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source_code = f.read()
                        Log.info(f'Original Source code {file}:')
                        Log.info(source_code)
                        Log.info('-' * 40)  # Prints a dividing line

                        Log.info(f'Fixed Source Code:')
                        message_template = Fixer42CrunchTemplate.fixer_42crunch_template(source_code)
                        chat_response = ChatClient().ask(message_template, ChatClientParams())
                        Log.info(chat_response)
                except Exception as e:
                    logging.error(f'Could not read file {file_path}: {e}')
                    traceback.print_exc()





