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
        self.node_to_id = {
            "Node1": {
                "Lightpath": [2269, 2270, 2273, 2275, 2283, 2286, 2291, 2295],
                "Service-1Gb": [2272, 2274, 2279, 2280, 2282, 2284, 2287, 2288, 2289, 2290, 2292, 2294],
                "Service-10Gb": [2271, 2276, 2277, 2278, 2281, 2285, 2293, 2296],
            },
            "Node2": {
                "Lightpath": [2297, 2298, 2301, 2303, 2311, 2314, 2319, 2323],
                "Service-1Gb": [2300, 2302, 2307, 2308, 2310, 2312, 2315, 2316, 2317, 2318, 2320, 2322],
                "Service-10Gb": [2299, 2304, 2305, 2306, 2309, 2313, 2321, 2324],
            },
            "Node3": {
                "Lightpath": [2357, 2358, 2361, 2363, 2371, 2374, 2379, 2383],
                "Service-1Gb": [2360, 2362, 2367, 2368, 2370, 2372, 2375, 2376, 2377, 2378, 2380, 2382],
                "Service-10Gb": [2359, 2364, 2365, 2366, 2369, 2373, 2381, 2384],
            },
        }

    def verify(self, data: dict):
        schema_files = self._load_schemas()
        errors = []
        for file_name, schema in schema_files.items():
            try:
                validate(data, schema)
                return (True, schema)
            except ValidationError as e:
                errors.append(f"Mismatch in {file_name} schema. Error message: {e.message}")
        return (False, errors)

    def score(self, data_list: list[dict], ground_truth_list: list[dict]) -> str:
        if len(data_list) != len(ground_truth_list):
            return f"Data and ground truth lists are not of the same length. Data length: {len(data_list)}, Ground truth length: {len(ground_truth_list)}"
        error_report = []
        for data, ground_truth in zip(data_list, ground_truth_list):
            res, schema = self.verify(data)
            if not res:
                return f"Data does not match any schema, {schema}"
            if not data == ground_truth:

                keys_truth = set(ground_truth.keys())
                keys_data = set(data.keys())
                _, err = self._compare_json_with_schema(data, ground_truth, schema)
                error_report += err
                for key in keys_data & keys_truth:
                    if data[key] != ground_truth[key]:
                        error_report.append(
                            f"Value for key {key} does not match ground truth. Predicted value: {data[key]}, Ground truth value: {ground_truth[key]}"
                        )
        return "\n".join(error_report)

    def _load_schemas(self) -> dict:
        schema_files = os.listdir(self._schema_dir)
        schemas = {}
        for schema_file in schema_files:
            with open(os.path.join(self._schema_dir, schema_file)) as f:
                schema = json.load(f)
                Draft202012Validator.check_schema(schema)
                schemas[schema_file] = schema
        return schemas

    def _parse_llm_output(self, json_string: str):
        start_index = json_string.find("```json\n")
        if start_index == -1:  # No JSON block found
            raise json.JSONDecodeError("Error in parsing JSON", json_string, 0)

        end_index = json_string.find("\n```", start_index)
        if end_index == -1:  # No closing backticks found
            raise json.JSONDecodeError("Error in parsing JSON", json_string, 0)

        json_body = json_string[start_index + 8 : end_index]  # Extract the JSON part

        return json.loads(json_body)

    def _compare_json_with_schema(self, json1, json2, schema):
        error_log = []

        def add_error(key_path, reason):
            nonlocal error_log
            error_log.append(f"{key_path}: {reason}")

        def compare_nested(json1, json2, schema, key_path=""):
            for key, schema_value in schema["properties"].items():
                new_key_path = key_path + "." + key if key_path else key
                if key in json1:
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
                elif key in json2 and key not in json1:
                    add_error(new_key_path, "Missing key in predicted JSON")

            return True  # Only reached if no mismatches were found

        result = compare_nested(json1, json2, schema)
        return result, error_log
