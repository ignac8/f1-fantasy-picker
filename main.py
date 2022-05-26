import itertools

import requests


def budget_filter(combination):
    driver_price = sum(map(lambda driver: driver['price'], combination[0]))
    constructor_price = combination[1]['price']
    budget = 100
    is_budget_right = driver_price + constructor_price < budget
    is_turbo_okay = combination[0][combination[2]]['price'] < 20
    return is_budget_right and is_turbo_okay


def get_points(combination):
    driver_points = sum(map(lambda x: get_points_for_player(x, combination[2]), enumerate(combination[0])))
    constructor_points = combination[1]['season_score']
    return driver_points + constructor_points


def get_points_for_player(x, y):
    season_score = x[1]['season_score']
    if x[0] == y:
        return 2 * season_score
    else:
        return season_score


if __name__ == '__main__':
    json = requests.get("https://fantasy-api.formula1.com/f1/2022/players").json()['players']
    drivers = list(filter(lambda x: x['position'] == 'Driver', json))
    constructors = list(filter(lambda x: x['position'] == 'Constructor', json))
    all_combinations = list(itertools.product(itertools.combinations(drivers, 5), constructors, range(5)))
    possible_combinations = list(filter(budget_filter, all_combinations))
    best_combination = max(possible_combinations, key=get_points)
    worst_combination = min(possible_combinations, key=get_points)
    debug = True
