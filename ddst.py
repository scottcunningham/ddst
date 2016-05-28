#!/usr/bin/env python
import sys
import re
import time
import datetime
import subprocess
from hurry.filesize import size, si

# 3078537+0 records in
RECORDS_IN_REGEX = re.compile("(\d+)\+(\d) records in")
# 3078536+0 records out
RECORDS_OUT_REGEX = re.compile("(\d+)\+(\d) records out")
# 1576210432 bytes transferred in 965.629548 secs (1632314 bytes/sec)
BYTES_TRANSFERRED_REGEX = re.compile("(\d+) bytes transferred in (\d+\.\d+) secs \((\d+) bytes/sec\)")


def loop(sleep_secs=5):
    subprocess.call(["sudo", "killall", "-INFO", "dd"])

    # We have to read these lines to skip them, maybe we can make use of them later
    records_in_line = sys.stdin.readline().strip()
    match = RECORDS_IN_REGEX.match(records_in_line)
    # print 'in:', match.group(1), '+', match.group(2)

    records_out_line = sys.stdin.readline().strip()
    match = RECORDS_OUT_REGEX.match(records_out_line)
    # print 'out:', match.group(1), '+', match.group(2)

    bytes_transferred_line = sys.stdin.readline().strip()
    match = BYTES_TRANSFERRED_REGEX.match(bytes_transferred_line)
    transferred = int(match.group(1))
    transferred = size(transferred, system=si)
    seconds = float(match.group(2))
    duration = "{:0>8}".format(datetime.timedelta(seconds=seconds))
    bytes_per_sec = float(match.group(3))
    bytes_per_sec = size(bytes_per_sec, system=si)
    print "Transferred", transferred, 'in', duration, "({}/sec)".format(bytes_per_sec)

    time.sleep(sleep_secs)


if __name__ == "__main__":
    while True:
        loop()
        # TODO: find out if piping program finished
        # (check if stdout closed?)
