import json

from llm_orchestrator.verifier import Verifier


def test_verifier():
    verifier = Verifier(schema_dir="data/json_schemas")
    res, _ = verifier.verify({"name": "John"})
    assert not res


def test_answer_parser():
    verifier = Verifier(schema_dir="data/json_schemas")

    json_1 = """
    {
        "product_name": "Awesome Wireless Headphones",
        "rating": 4.5,
        "review_text": "Great sound quality and comfortable to wear. Long battery life too!"
    }
    """
    json_2 = """
    {
        "product_name": "Mediocre Wireless Headphones",
        "rating": 3.0,
        "review_text": "It's not much, but it's a honest job"
    }
    """
    json_to_match = [json.loads(json_1), json.loads(json_2)]
    test_to_parse = f"""
    I suggest the following product review:
    ```json
            {json_1}
    ```

    And here is another one:
    ```json
            {json_2}
    ```
    """

    json_list = verifier._parse_llm_output(test_to_parse)
    assert json_list == json_to_match
