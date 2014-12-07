import pytest

from pairings import fill_recipients

def test_optimal_solution():
    user_data = [{'fields': {'profile': 'Tom',
                             'partner': None,
                             'avoid': ['Dick'],
                             'prefer': ['Harry']}},
                {'fields': {'profile': 'Dick',
                            'partner': None,
                            'avoid': ['Harry'],
                            'prefer': ['Tom']}},
                {'fields': {'profile': 'Harry',
                            'partner': None,
                            'avoid': ['Tom'],
                            'prefer': ['Dick']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['fields']['recipient'] == user['fields']['prefer'][0]

def test_extra_fields():
    user_data = [
        {'fields': {'profile': 'Tom',
                     'partner': None,
                     'magic': 'Bus',
                     'avoid': ['Dick'],
                     'prefer': ['Harry']}},
        {'fields': {'profile': 'Dick',
                    'partner': None,
                    'fatal': 'Book',
                    'avoid': ['Harry'],
                    'prefer': ['Tom']}},
        {'fields': {'profile': 'Harry',
                    'partner': None,
                    'ice': 'Cream',
                    'avoid': ['Tom'],
                    'prefer': ['Dick']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['fields']['recipient'] == user['fields']['prefer'][0]

def test_forbidden():
    user_data = [
        {'fields': {'profile': 'Tom',
                     'partner': 'Dick',
                     'avoid': ['Joe'],
                     'prefer': ['Harry']}},
         {'fields': {'profile': 'Dick',
                     'partner': 'Tom',
                     'avoid': ['Harry'],
                     'prefer': ['Joe']}},
         {'fields': {'profile': 'Harry',
                     'partner': None,
                     'avoid': ['Dick'],
                     'prefer': ['Tom']}},
         {'fields': {'profile': 'Joe',
                     'partner': None,
                     'avoid': ['Dick'],
                     'prefer': ['Harry']}},
         {'fields': {'profile': 'Douche',
                     'partner': None,
                     'avoid': ['Joe'],
                     'prefer': ['Dick']}},
         {'fields': {'profile': 'Princess',
                     'partner': None,
                     'avoid': ['Joe'],
                     'prefer': ['Dick']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['fields']['recipient'] != user['fields']['profile']
        assert user['fields']['recipient'] != user['fields']['partner']

if __name__ == '__main__':
    pytest.main()
