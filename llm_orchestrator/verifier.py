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

    def verify(self, data: dict) -> tuple[bool, str]:
        schema_files = self._load_schemas()
        errors = []
        for file_name, schema in schema_files.items():
            try:
                validate(data, schema)
                return (True, schema)
            except ValidationError as e:
                errors.append(f"Mismatch in {file_name} schema. Error message: {e.message}")
        return (False, errors)

    def score(self, data_list: list[dict], ground_truth_list: list[dict]) -> tuple[int, str]:
        if len(data_list) != len(ground_truth_list):
            return (
                0,
                f"Data and ground truth lists are not of the same length. Lengths: {len(data_list)} and {len(ground_truth_list)}",
            )
        for data, ground_truth in zip(data_list, ground_truth_list):
            res, schema = self.verify(data)
            if not res:
                return (0, f"Data does not match any schema, {schema}")
            if not data == ground_truth:
                error_report = []
                keys_truth = set(ground_truth.keys())
                keys_data = set(data.keys())
                _, err = self._compare_json_with_schema(data, ground_truth, schema)
                error_report += err
                for key in keys_data & keys_truth:
                    if data[key] != ground_truth[key]:
                        error_report.append(f"Value for key {key} does not match ground truth")
                return (0, "\n".join(error_report))
        return (1, "Data matches ground truth")

    def _load_schemas(self) -> dict:
        schema_files = os.listdir(self._schema_dir)
        schemas = {}
        for schema_file in schema_files:
            with open(os.path.join(self._schema_dir, schema_file)) as f:
                schema = json.load(f)
                Draft202012Validator.check_schema(schema)
                schemas[schema_file] = schema
        return schemas

    def _parse_llm_output(self, json_string: str) -> list:
        json_list = []
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

    def _compare_json_with_schema(self, json1, json2, schema):
        error_log = []

        def add_error(key_path, reason):
            nonlocal error_log
            error_log.append(f"{key_path}: {reason}")

        def compare_nested(json1, json2, schema, key_path=""):
            for key, schema_value in schema["properties"].items():
                new_key_path = key_path + "." + key if key_path else key
                if key not in json2:
                    if "default" in schema_value and json1[key] == schema_value["default"]:
                        continue
                    else:
                        add_error(new_key_path, "Key missing in second JSON")
                        return False  # Stop recursion if a mismatch is found
                elif isinstance(json1[key], dict) and isinstance(json2[key], dict):
                    if not compare_nested(json1[key], json2[key], schema_value, new_key_path):
                        return False
                else:
                    if json1[key] != json2[key]:
                        add_error(new_key_path, "Value mismatch")
                        return False

            return True  # Only reached if no mismatches were found

        result = compare_nested(json1, json2, schema)
        return result, error_log
