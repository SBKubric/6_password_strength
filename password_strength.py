import re

def check_if_in_blacklist(password):
    with open('password_list') as password_list:
        blacklist = re.findall(r'\w+', password_list.read())
        for pas in blacklist:
            if password.lower() == pas:
                return True
    return False


def check_for_errors(password):
    blacklist_error = check_if_in_blacklist(password)
    len_error = len(password) < 6
    long_check = len(password) >= 10
    digit_error = re.search(r'[0-9]', password) is None
    lowercase_error = re.search(r'[a-z]', password) is None
    uppercase_error = re.search(r'[A-Z]', password) is None
    special_error = re.search(r'\W', password) is None

    return {
        'blacklist_error' : blacklist_error,
        'len_error' : len_error,
        'long_check' : long_check,
        'digit_error' : digit_error,
        'lowercase_error' : lowercase_error,
        'uppercase_error' : uppercase_error,
        'special_error' : special_error,
    }


def get_password_strength(check_results):
    if check_results['blacklist_error']:
        return 1
    if check_results['len_error']:
        return 2
    sum = 3
    if check_results['long_check']:
        sum += 2
    if not check_results['digit_error']:
        sum += 1
    if not check_results['lowercase_error']:
        sum += 1
    if not check_results['uppercase_error']:
        sum += 1
    if not check_results['special_error']:
        sum += 2
    return sum


if __name__ == '__main__':
    pwd = ''
    print('Enter your password:')
    while pwd == '':
        pwd = input()
    res = get_password_strength(check_for_errors(pwd))
    print('Password strength is %s out of 10.' % res)
