#!/usr/bin/env python

# ----------------------------------------------------------------------
# app.py
# Author: Theo Knoll, Henry Knoll, Brett Zeligson
# For use in running the program locally
# ----------------------------------------------------------------------

from sys import argv, exit, stderr
from flask_app import app


# Below code is from Princeton University Professor
# Bob Dondero's runserver.py example program
def main():
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[1])
    except Exception:
        print('Port must be an integer.', file=stderr)
        exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()