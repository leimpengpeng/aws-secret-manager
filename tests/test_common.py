# content of test_sysexit.py
import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret_manager.util import parse_namespace

def test_parse_namespace():
    expected_name = ['ew1-proj-ci', 
        'ew1-proj-prd',
        'ane1-proj-prd',
        'ew1-proj-dev-devname',
    ]
    test_valid_names = ['ew1-proj-ci/abc', 
        'ew1-proj-prd/123',
        'ane1-proj-prd/efg',
        'ew1-proj-dev-devname/xyz',
    ]
    # 1. Test valid secret name
    for name in test_valid_names:
        assert parse_namespace(name) in expected_name

    with pytest.raises(ValueError, match=r"Invalid format for the secret name: 'ane1-proj-prdefg', prefix is required"):
        parse_namespace('ane1-proj-prdefg')
    with pytest.raises(ValueError, match=r"Invalid prefix format: 'ane1-proj-pred'"):
        parse_namespace('ane1-proj-pred/abc')
    with pytest.raises(ValueError, match=r"Invalid prefix format: 'proj-dev'"):
        parse_namespace('proj-dev/abc')
