import json
import os
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
