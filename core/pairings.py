'''Assign Santas to people.'''

from random import choice
from enum import Enum
from itertools import permutations

class Weight(Enum):
    positive = 1.5
    neutral = 1.0
    negative = 0.5
    forbidden = 0.0

class Weights:
    def __init__(self, users):
        weights = []
        for index, user in enumerate(users):
            row = len(users) * [Weight.neutral]
            row[index] = Weight.forbidden
            if user['fields']['partner']:
                row[users.index(user['fields']['partner'])] = Weight.forbidden
            for avoid in user['fields']['avoid']:
                row[users.index(avoid)] = Weight.negative
            for prefer in user['fields']['prefer']:
                print('Prefer list', prefer)
                print('Users list', users.users)
                row[users.index(prefer)] = Weight.positive
            weights.append(row)
        self.weights = weights

    def __getitem__(self, key):
        return self.weights[key]

class Solver:
    def __init__(self, users):
        self.profiles = users.profiles
        self.weights = Weights(users)

    def product(self, permutation):
        score = 1.0
        for index, profile in enumerate(permutation):
            score *= self.weights[index][self.profiles.index(profile)].value
        return score

    def solve(self):
        best_score = 0
        best_permutations = []
        for permutation in permutations(self.profiles):
            score = self.product(permutation)
            if score:
                if score == best_score:
                    best_permutations.append(permutation)
                elif score > best_score:
                    best_score = score
                    best_permutations = [permutation]
        return choice(best_permutations)

class Users:
    def __init__(self, users):
        self.users = users
        self.profiles = [user['fields']['profile'] for user in self.users]

    def __iter__(self):
        return iter(self.users)

    def __len__(self):
        return len(self.users)

    def index(self, profile):
        return self.profiles.index(profile)

    def set_recipients(self, recipients):
        for user, recipient in zip(self.users, recipients):
            user['fields']['recipient'] = recipient

def fill_recipients(user_data):
    users = Users(user_data)
    solver = Solver(users)
    recipients = solver.solve()
    users.set_recipients(recipients)
