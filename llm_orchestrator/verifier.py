import json
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
        self.schema_dir = schema_dir

    def verify(self, data: str):
        schema = self._load_schema()
        data = json.loads(data)
        try:
            validate(data, schema)
        except ValidationError as e:
            return e.message

    def score(self, data: str):
        res = self.verify(data)
        if res:
            return 0
        return 1

    def _load_schema(self) -> dict:
        with open(self.schema_dir) as f:
            schema = json.load(f)
            Draft202012Validator.check_schema(schema)
            return schema
