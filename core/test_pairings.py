import pytest

from pairings import fill_recipients

def test_optimal_solution():
    user_data = [
        {'fields': {'profile': 'Tom',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Dick'],
                    'prefer': ['Harry']}},
        {'fields': {'profile': 'Dick',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Harry'],
                    'prefer': ['Tom']}},
        {'fields': {'profile': 'Harry',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Tom'],
                    'prefer': ['Dick']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['fields']['recipient'] == user['fields']['prefer'][0]

def test_avoid_partner():
    user_data = [
        {'fields': {'profile': 'Tom',
                    'partner': 'Dick',
                    'avoid_partner': False,
                    'avoid': [],
                    'prefer': ['Dick']}},
        {'fields': {'profile': 'Dick',
                    'partner': 'Tom',
                    'avoid_partner': True,
                    'avoid': [],
                    'prefer': ['Harry']}},
        {'fields': {'profile': 'Harry',
                    'partner': None,
                    'avoid': [],
                    'prefer': ['Joe']}},
        {'fields': {'profile': 'Joe',
                    'partner': None,
                    'avoid': [],
                    'prefer': ['Harry']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        if user['fields'].get('avoid_partner', False):
            assert user['fields']['recipient'] != user['fields']['partner']

def test_extra_fields():
    user_data = [
        {'fields': {'profile': 'Tom',
                    'partner': None,
                    'avoid_partner': True,
                    'magic': 'Bus',
                    'avoid': ['Dick'],
                    'prefer': ['Harry']}},
        {'fields': {'profile': 'Dick',
                    'partner': None,
                    'avoid_partner': True,
                    'fatal': 'Book',
                    'avoid': ['Harry'],
                    'prefer': ['Tom']}},
        {'fields': {'profile': 'Harry',
                    'partner': None,
                    'avoid_partner': True,
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
                    'avoid_partner': True,
                    'avoid': ['Joe'],
                    'prefer': ['Harry']}},
        {'fields': {'profile': 'Dick',
                    'partner': 'Tom',
                    'avoid_partner': True,
                    'avoid': ['Harry'],
                    'prefer': ['Joe']}},
        {'fields': {'profile': 'Harry',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Dick'],
                    'prefer': ['Tom']}},
        {'fields': {'profile': 'Joe',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Dick'],
                    'prefer': ['Harry']}},
        {'fields': {'profile': 'Douche',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Joe'],
                    'prefer': ['Dick']}},
        {'fields': {'profile': 'Princess',
                    'partner': None,
                    'avoid_partner': True,
                    'avoid': ['Joe'],
                    'prefer': ['Dick']}},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['fields']['recipient'] != user['fields']['profile']
        assert user['fields']['recipient'] != user['fields']['partner']

if __name__ == '__main__':
    pytest.main()
