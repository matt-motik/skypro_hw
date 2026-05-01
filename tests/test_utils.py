import json
import os
import tempfile

import pytest

from src.utils import read_json_file


@pytest.mark.parametrize(
    "n, data, expected_result",
    [
        (None, None,[]),
        ('', None, []),
        ('wrong/path.json', None,[]),
        ('temp.json', None, []),
        ('temp.json', """{"answer": 42 }""", []),
        ('temp.json', """Non JSON data, or error in JSON""", []),
        ('temp.json', """[ {"id": 0} , {"id": 2} ]""", [ {'id': 0}, {'id': 2} ]),
    ],
)

def test_read_json_file(n, data, expected_result):
    if n == 'temp.json':
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_json = os.path.join(tmpdir,"temp.json")
            if data:
                with open(temp_json, "w", encoding="utf-8") as f:
                    f.write(data)
            assert read_json_file(temp_json) == expected_result
    else:
        assert read_json_file(n) == expected_result