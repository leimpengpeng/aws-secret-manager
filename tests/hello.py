import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# if __name__ == '__main__':
#     parse_namespace('124')

test_names = ['ew1-proj-ci/abc', 
    'ew1-proj-prd/123',
    'ane1-proj-prd/efg',
    'ew1-idprot-dev-devname/xyz',
]
expected_name = ['ew1-proj-ci', 
    'ew1-proj-prd',
    'ane1-proj-prd',
    'ew1-proj-dev-devname',
]
for name,id in test_names:
    print('name', 'id', name, id)