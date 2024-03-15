import argparse
import copy
import os
from enum import Enum
from typing import Optional, Self

from entrypoint.dto.generate_base_dto import GenerateBaseDto
from infrastructure.log import Log
from model.enums.model_type import ModelType

import jsons
from starlette_context import context


class ExecMode(Enum):
    COMMAND_LINE = "COMMAND_LINE"
    API = "API"


class ExecParameters():
    __instance: Self  # Only used when exec_mode = COMMAND_LINE
    __exec_mode: ExecMode = ExecMode.COMMAND_LINE

    feature_name: str
    entrypoint_files: list[str] = []
    entrypoint_files_type: Optional[ModelType] = None

    verbose: bool = False
    input_source_path = None

    @classmethod
    def instance(cls) -> Self:
        if ExecParameters.__exec_mode == ExecMode.API:
            return context["ExecParameters"]
        if ExecParameters.__exec_mode == ExecMode.COMMAND_LINE:
            return ExecParameters.__instance
        return None

    @classmethod
    def build_for_api(cls, params: GenerateBaseDto) -> Self:
        ExecParameters.__exec_mode = ExecMode.API

        context_instance = ExecParameters()
        context_instance.entrypoint_folder = params.entrypoint_folder
        context_instance.security_tool = params.security_tool
        context_instance.input_source_path = os.environ["INPUT_SOURCE_PATH"]
        context_instance.verbose = Log.is_verbose()

        context["ExecParameters"] = context_instance

        return context_instance

    @classmethod
    def build_for_command_line(cls, args: argparse.Namespace) -> Self:
        ExecParameters.__exec_mode = ExecMode.COMMAND_LINE

        ExecParameters.__instance = ExecParameters()
        ExecParameters.__instance.entrypoint_folder = args.entrypoint_folder
        ExecParameters.__instance.security_tool = args.security_tool

        ExecParameters.__instance.verbose = args.verbose
        ExecParameters.__instance.input_source_path = os.environ["INPUT_SOURCE_PATH"]

        return ExecParameters.__instance

    def has_something_todo(self):
        return self.entrypoint_folder or \
            self.security_tool

    def validate(self) -> list[str]:
        result = []

        if not self.has_something_todo():
            msg = "Nothing to do, you must specify at least one of \
--entrypoint_folder or --security_tool"
            Log.error(msg)
            result.append(msg)

        return result

    def __str__(self):
        new_self = copy.deepcopy(self)
        new_self.__instance = None

        return jsons.dumps(new_self, {"indent": 4})

    __repr__ = __str__
