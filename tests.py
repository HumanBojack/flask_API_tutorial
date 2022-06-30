import json
from helpers import decode_json


def test_json_decoder():
  json_object = decode_json(b'{"data": {"numbers": [0, 1, 2, 3, 4, 5], "characters": ["a", "b", "c"]}}')
  # Assertions on the dict
  assert isinstance(json_object, dict)
  assert json_object['data']['numbers'][2] == 2
  assert json_object['data']['characters'][2] == "c"
  