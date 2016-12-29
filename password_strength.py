import re
import os
import urllib.request as request
import argparse
import getpass


def parse_args():
    parser = argparse.ArgumentParser(description='The script is designed for estimating strength of your password.')
    parser.add_argument('-u', '--url', default='https://github.com/SBKubric/SecLists/raw/master/'
                                               'Passwords/10_million_password_list_top_1000000.txt',
                        help='The url to the location of the blacklist file with passwords.')
    parser.add_argument('-bl', '--blacklist', default='./password_list', help='The local location of the blacklist'
                                                                              'with passwords.')
    return parser.parse_args()


def upload_blacklist(path, url):
    request.urlretrieve(url, path)


def check_if_in_blacklist(password, blacklist_location):
    with open(blacklist_location) as password_list:
        blacklist = re.findall(r'\w+', password_list.read())
    if password.lower() in blacklist:
        return True


def check_for_errors(password, blacklist_location):
    return {
        'blacklist_check': check_if_in_blacklist(password, blacklist_location),
        'short_password_check': len(password) < 6,
        'long_password_check': len(password) >= 10,
        'digit_check': re.search(r'[0-9]', password) is not None,
        'lowercase_check': re.search(r'[a-z]', password) is not None,
        'uppercase_check': re.search(r'[A-Z]', password) is not None,
        'special_check': re.search(r'\W', password) is not None,
    }


def get_password_strength(check_results):
    if check_results['blacklist_check']:
        return 1
    if check_results['short_password_check']:
        return 2
    sum = 3
    if check_results['long_password_check']:
        sum += 2
    if check_results['digit_check']:
        sum += 1
    if check_results['lowercase_check']:
        sum += 1
    if check_results['uppercase_check']:
        sum += 1
    if check_results['special_check']:
        sum += 2
    return sum


if __name__ == '__main__':
    url_default = 'https://github.com/SBKubric/SecLists/raw/master/' \
                  'Passwords/10_million_password_list_top_1000000.txt'
    args = parse_args()
    print('Checking if there is a local copy of the blacklist_file...')
    if not os.path.isfile(args.blacklist) or args.url != url_default:
        print('Downloading the blacklist_file...')
        upload_blacklist(args.blacklist, args.url)
    pwd = getpass.getpass('Enter your password:\n=> ')
    while pwd == '':
        print()
        pwd = getpass.getpass('The password can\'t have zero length!\n=> ')
    print('Password strength is %s out of 10.' % get_password_strength(check_for_errors(pwd, args.blacklist)))
