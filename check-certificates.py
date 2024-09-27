import sys

from ssl_cert_checker.check_tools import check_certificates
from ssl_cert_checker.check_tools import EXIT_NO_HOST_LIST

if __name__ == '__main__':

    endpoints = sys.argv[1:]

    if len(endpoints):
        results = check_certificates(endpoints)
        print(results[0])
        sys.exit(results[1])
    else:
        print('Usage: {} <list of endpoints>'.format(sys.argv[0]))
        sys.exit(EXIT_NO_HOST_LIST)
