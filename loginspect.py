#!/bin/python

import tomllib
import sys
import re

RESET = '\x1b[0m'
UNDERLINE = '\x1b[4m'
BOLD = '\x1b[1m'
FG_ID = '\x1b[38;5;{}m'
FG_YELLOW_B = '\x1b[93m'
IP_COLORS = [197, 201, 67, 77, 121, 221, 208]

pat = re.compile(r"(^\d+\.\d+\.\d+\.\d+) - - \[([^]]*)\] \"GET (.*) HTTP/1\.0\" (\d+).*$")

with open("config.toml", "rb") as file:
    conf = tomllib.load(file)
    excl_ips = conf["excluded_ips"]

filter_ip = sys.argv[1] if 1 < len(sys.argv) else None

ips = {}
color_i = 0
last_day = ""

while True:
    try:
        inp = input()
        if match := pat.match(inp):
            ip, date, uri, status = match.groups()
            day, time = date.split()

            if not filter_ip or ip == filter_ip:
                if day != last_day:
                    if last_day != "":
                        print()
                    print(f"{BOLD}[{day}]{RESET}")
                last_day = day

            if ip not in excl_ips and status == "200":
                if ip not in ips:
                    ips[ip] = [1, FG_ID.format(IP_COLORS[color_i])]
                    color_i = (color_i + 1) % len(IP_COLORS)
                else:
                    ips[ip][0] += 1
                
                if not filter_ip or filter_ip == ip:
                    print(f"{ips[ip][1]}{ip:15}{RESET}  {time}  \
{FG_YELLOW_B}{uri}{RESET}")

    except EOFError:
        break

if not filter_ip:
    print(f"\n{UNDERLINE}ip address{RESET}       {UNDERLINE}occurences{RESET}")
    for ip, occ_col in sorted(ips.items(), key=lambda x: x[1][0], reverse=True):
        occurences, color = occ_col
        if 1 < occurences:
            print(f"{color}{ip:15}{RESET}  {occurences}")

