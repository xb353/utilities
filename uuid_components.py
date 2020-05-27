import uuid
import sys
from datetime import datetime as dt

# For Reference
# https://en.wikipedia.org/wiki/Universally_unique_identifier
# https://tools.ietf.org/html/rfc4122

# this script is primarily for rfc4122 version 1 UUID's to extract the time and mac address

# UUID Timestamps are number of nanoseconds from
# 60-bit timestamp, being the number of 100-nanosecond intervals since midnight 15 October 1582 Coordinated Universal Time (UTC), the date on which the Gregorian calendar was first adopted

# Inspired From:
# https://dabblingwithdata.wordpress.com/2018/10/13/extracting-the-date-and-time-a-uuid-was-created-with-bigquery-sql-with-a-brief-foray-into-the-history-of-the-gregorian-calendar/

SECONDS_UNTIL_EPOCH = 12219292800

def main(u):
    VALID = True

    U = uuid.UUID(u)

    # Nanoseconds to Seconds
    t = U.time / 10_000_000

    # Convert to epoch by subtracting the number of seconds between 15 October 1582 and 1 January 1970
    t = t - SECONDS_UNTIL_EPOCH

    # Get a timestamp from the datetime module
    timestamp = str(dt.fromtimestamp(t))

    # Attempt to get MAC Address
    poss_mac = U.fields[-1]

    # Check if least significant bit of first octet is a 1 or a 0
    # If it's a 1, this evaluates to true, and it's not a valid MAC Address
    if (poss_mac>>40) % 2:
        VALID = False

    variant = U.variant
    version = U.version

    print(f"\n\t UUID: {U}")
    print(f"\t Variant: {variant}")
    print(f"\t Version: {version}")
    print(f"\t Timestamp: {timestamp}")
    print(f"\t Mac Address: {hex(poss_mac)[2:]}, Valid: {VALID}")

if __name__ == "__main__":
    if len(sys.argv)<=2:
        print("Please provide one or more UUIDs as arguments.")
        sys.exit(0)
    for u in sys.argv[1:]:
        main(u)
