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
            if user['partner']:
                row[users.index(user['partner'])] = Weight.forbidden
            for avoid in user['avoid']:
                row[users.index(avoid)] = Weight.negative
            for prefer in user['prefer']:
                row[users.index(prefer)] = Weight.positive
            weights.append(row)
        self.weights = weights

    def __getitem__(self, key):
        return self.weights[key]

class Solver:
    def __init__(self, users):
        self.names = users.names
        self.weights = Weights(users)

    def product(self, permutation):
        score = 1.0
        for index, name in enumerate(permutation):
            score *= self.weights[index][self.names.index(name)].value
        return score

    def solve(self):
        best_score = 0
        best_permutations = []
        for permutation in permutations(self.names):
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
        self.names = [user['name'] for user in self.users]

    def __iter__(self):
        return iter(self.users)

    def __len__(self):
        return len(self.users)

    def index(self, name):
        return self.names.index(name)

    def set_recipients(self, recipients):
        for user, recipient in zip(self.users, recipients):
            user['recipient'] = recipient

def fill_recipients(user_data):
    users = Users(user_data)
    solver = Solver(users)
    recipients = solver.solve()
    users.set_recipients(recipients)
