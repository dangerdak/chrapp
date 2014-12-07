import pytest

from pairings import fill_recipients

def test_optimal_solution():
    user_data = [
        {'name': 'Tom',
         'partner': None,
         'avoid': ['Dick'],
         'prefer': ['Harry']},
        {'name': 'Dick',
         'partner': None,
         'avoid': ['Harry'],
         'prefer': ['Tom']},
        {'name': 'Harry',
         'partner': None,
         'avoid': ['Tom'],
         'prefer': ['Dick']},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['recipient'] == user['prefer'][0]

def test_forbidden():
    user_data = [
        {'name': 'Tom',
         'partner': 'Dick',
         'avoid': ['Joe'],
         'prefer': ['Harry']},
        {'name': 'Dick',
         'partner': 'Tom',
         'avoid': ['Harry'],
         'prefer': ['Joe']},
        {'name': 'Harry',
         'partner': None,
         'avoid': ['Dick'],
         'prefer': ['Tom']},
        {'name': 'Joe',
         'partner': None,
         'avoid': ['Dick'],
         'prefer': ['Harry']},
        {'name': 'Douche',
         'partner': None,
         'avoid': ['Joe'],
         'prefer': ['Dick']},
        {'name': 'Princess',
         'partner': None,
         'avoid': ['Joe'],
         'prefer': ['Dick']},
    ]
    fill_recipients(user_data)
    for user in user_data:
        assert user['recipient'] != user['name']
        assert user['recipient'] != user['partner']

if __name__ == '__main__':
    pytest.main()
