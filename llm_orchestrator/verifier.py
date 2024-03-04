import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator


class AbstractVerifier(ABC):
    @abstractmethod
    def verify(self, data: Any) -> Any:
        pass


class Verifier(AbstractVerifier):
    def __init__(self, schema_dir: str):
        self._schema_dir = schema_dir

    def verify(self, data: str) -> tuple[bool, str]:
        schema_files = self._load_schemas()
        data = json.loads(data)
        errors = ""
        for file_name, schema in schema_files.items():
            try:
                validate(data, schema)
                return (True, "")
            except ValidationError as e:
                errors += f"Mismatch in {file_name} schema. Error message: {e.message}\n"
        return (False, errors)

    def score(self, data: str):
        res, _ = self.verify(data)
        if res:
            return 1
        return 0

    def _load_schemas(self) -> dict:
        schema_files = os.listdir(self._schema_dir)
        schemas = {}
        for schema_file in schema_files:
            with open(os.path.join(self._schema_dir, schema_file)) as f:
                schema = json.load(f)
                Draft202012Validator.check_schema(schema)
                schemas[schema_file] = schema
        return schemas

    def _parse_llm_output(self, json_string: str) -> list:  # Changed return type to a list
        json_list = []  # To store the parsed JSON objects
        # Updated regular expression for multiple matches
        pattern = r"""```    # match first occuring triple backticks
                    (?:json)? # zero or one match of string json in non-capturing group
                    (.*?)     # non-greedy match to the next triple backticks
                    ```       # match the closing backticks
                    """
        for match in re.finditer(pattern, json_string, flags=re.DOTALL | re.VERBOSE):
            json_str = match.group(1).strip()

            try:
                parsed = json.loads(json_str, strict=False)
                json_list.append(parsed)
            except json.JSONDecodeError:
                print(f"Invalid JSON found: {json_str}")

        return json_list
