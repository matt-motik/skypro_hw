import json
import os
import tempfile

import pytest

from src.utils import read_json_file


@pytest.mark.parametrize(
    "file_path, data, expected_result",
    [
        (None, None,[]),
        ('', None, []),
        ('wrong/path.json', None,[]),
        ('temp.json', "", []),
        ('temp.json', """{"answer": 42 }""", []),
        ('temp.json', """Non JSON data, or error in JSON""", []),
        ('temp.json', """[ {"id": 0} , {"id": 2} ]""", [ {'id': 0}, {'id': 2} ]),
    ],
)

def test_read_json_file(file_path, data, expected_result):
    if file_path == 'temp.json':
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_json = os.path.join(tmpdir,"temp.json")
            if data is not None:
                with open(temp_json, "w", encoding="utf-8") as f:
                    f.write(data)
            assert read_json_file(temp_json) == expected_result
    else:
        assert read_json_file(file_path) == expected_result