import re
import os
import urllib.request as request
import argparse
import getpass

global blacklist_location
global url_default


def parse_args():
    parser = argparse.ArgumentParser(description='The script is designed for estimating strength of your password.')
    parser.add_argument('-u', '--url', default='https://github.com/SBKubric/SecLists/raw/master/'
                                               'Passwords/10_million_password_list_top_1000000.txt',
                        help='The url to the location of the blacklist file with passwords.')
    parser.add_argument('-bl', '--blacklist', default='./password_list', help='The local location of the blacklist'
                                                                              'with passwords.')
    return parser.parse_args()


def set_blacklist(path, url, *, do_upload=False):
    print('Checking if there is a local copy of the blacklist_file...')
    if os.path.isfile(path) and not do_upload:
        return None
    print('Downloading the blacklist_file...')
    request.urlretrieve(url, 'password_list')


def check_if_in_blacklist(password):
    with open(blacklist_location) as password_list:
        blacklist = re.findall(r'\w+', password_list.read())
    if password.lower() in blacklist:
        return True


def check_for_errors(password):
    blacklist_error = check_if_in_blacklist(password)
    len_error = len(password) < 6
    long_check = len(password) >= 10
    digit_error = re.search(r'[0-9]', password) is None
    lowercase_error = re.search(r'[a-z]', password) is None
    uppercase_error = re.search(r'[A-Z]', password) is None
    special_error = re.search(r'\W', password) is None

    return {
        'blacklist_error': blacklist_error,
        'len_error': len_error,
        'long_check': long_check,
        'digit_error': digit_error,
        'lowercase_error': lowercase_error,
        'uppercase_error': uppercase_error,
        'special_error': special_error,
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
    url_default = 'https://github.com/SBKubric/SecLists/raw/master/' \
                  'Passwords/10_million_password_list_top_1000000.txt'
    args = parse_args()
    blacklist_location = args.blacklist
    set_blacklist(args.blacklist, args.url, do_upload=args.url != url_default)
    pwd = ''
    pwd = getpass.getpass('Enter your password:\n=> ')
    while pwd == '':
        print()
        pwd = getpass.getpass('The password can\'t have zero length!\n=> ')
    res = get_password_strength(check_for_errors(pwd))
    print('Password strength is %s out of 10.' % res)
