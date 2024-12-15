#!/usr/bin/env python3

# This script takes a a tag number, converts it
# to the number the board recorded via the
# wiegand protocol, and then looks up the
# info in the sqlite3 database.
import sys
import sqlite3
import wiegand_calculator.wiegand as wc

from datetime import datetime

# The database file is in the same directory as the script
# so we don't need to specify a path
DATABASE = "dooraccess.db"


def taglookup(tag):
    # Open the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Get the tag number
    door_tag = wc.convert_to_wiegand(tag)
    print(f"Looking up tag {tag} which is {door_tag}")
    # Get the tag info
    c.execute(
        f"SELECT event_ts, access, door, tag FROM access_event WHERE tag='{door_tag}'"
    )
    # Now print all the rows
    for row in c.fetchall():
        # Now let's format the output a bit. We'll use the
        # datetime module to format the timestamp
        # The event_ts field is formatted in
        # '2024-12-05 13:26:17 +0000 UTC' format

        event_ts = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S %z UTC")
        # Now we'll convert it to a more readable format, including
        # AM/PM
        event_ts = event_ts.strftime("%m/%d/%Y %I:%M:%S %p")
        access = "Granted" if row[1] == "01" else "Denied"
        door = "Front" if row[2] == "01" else "Back"
        tag = wc.convert_from_wiegand(row[3])
        # Now let's print it out in tabular format and pad it so
        # it looks nice
        print(f"{event_ts}\t{door}\t{access}")

    conn.close()


if __name__ == "__main__":
    # get the tag number as a parameter
    tag = int(sys.argv[1])
    taglookup(tag)
