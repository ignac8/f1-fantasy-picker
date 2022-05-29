import itertools

import requests

budget = 102.5
number_of_drivers = 5
with_mega_driver = False
required_drivers = []


def budget_filter(combination):
    driver_price = sum(map(lambda driver: driver['price'], combination[0]))
    constructor_price = combination[1]['price']
    is_budget_right = driver_price + constructor_price < budget
    is_turbo_okay = combination[0][combination[2]]['price'] < 20
    is_mega_okay = combination[0][combination[3]] != combination[0][combination[2]]
    has_required_drivers = all(map(lambda required_driver:
                                   any(map(lambda x: x['last_name'] == required_driver, combination[0])),
                                   required_drivers))
    return is_budget_right and is_turbo_okay and is_mega_okay and has_required_drivers


def calculate_points(combination):
    driver_points = sum(
        map(lambda x: get_points_for_player(x, combination[2], combination[3]),
            enumerate(combination[0])))
    constructor_points = combination[1]['season_score']
    total_points = driver_points + constructor_points
    return combination[0], combination[1], combination[2], combination[3], total_points


def get_points_for_player(driver, turbo_driver_num, mega_driver_num):
    season_score = driver[1]['season_score']
    if driver[0] == turbo_driver_num:
        return 2 * season_score
    elif driver[0] == mega_driver_num and with_mega_driver:
        return 3 * season_score
    else:
        return season_score


if __name__ == '__main__':
    json = requests.get("https://fantasy-api.formula1.com/f1/2022/players").json()['players']
    drivers = list(filter(lambda x: x['position'] == 'Driver', json))
    constructors = list(filter(lambda x: x['position'] == 'Constructor', json))
    all_combinations = itertools.product(
        itertools.combinations(drivers, number_of_drivers), constructors, range(number_of_drivers),
        range(number_of_drivers))
    possible_combinations = filter(lambda x: budget_filter(x), all_combinations)
    combinations_with_points = list(map(lambda x: calculate_points(x), possible_combinations))
    best_combination = max(combinations_with_points, key=lambda x: x[4])

    print(list(map(lambda x: x['last_name'] if x['last_name'] else x['first_name'], best_combination[0])))
    print(best_combination[1]['first_name'])
    print("TD: " + best_combination[0][best_combination[2]]['last_name'])
    if with_mega_driver:
        print("MD: " + best_combination[0][best_combination[3]]['last_name'])
