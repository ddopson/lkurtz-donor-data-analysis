#!/usr/bin/env python

import fileinput
from collections import defaultdict

ORGS = [
  'PEER',
  'UCS',
  'GAP',
  'POGO',
  'EPN',
  'CLIMATE',
  'PROTECT',
  'FIRE',
  'EFF']

DELIM="\t"

EXCLUDE = [
  "Fidelity Charitable Gift Fund",
  "Boston Foundation, Inc.",
  "Seattle Foundation",
  "The Energy Foundation",
  "The Minneapolis Foundation",
  "The San Francisco Foundation",
  "Foundation For The Carolinas",
  "Vanguard Charitable Endowment Program",
  "Schwab Charitable",
]

def fmt_dollar(dollar):
 return "${:,}".format(dollar)


def header():
  header = [
    "Donor",
    "Most Recent",
    "NumDonations",
    "NumOrgs",
    "MinDonation",
    "MaxDonation",
    "Total [Since 2016]",
    "Total [Before 2016]",
    "Summary [Since 2016]",
    "Summary [Before 2016]"]
  for org in ORGS:
    header.append(org)
    header.append(org)
  print DELIM.join(header)

def make_summary(counts, totals):
  stuff = reversed(sorted([
    [totals[org], counts[org], org]
    for org in ORGS
    if totals[org] > 0
  ]))
  return ", ".join([
    "{} x {}: ${:,}".format(s[1], s[2], s[0])
    for s in stuff])

rows = []
last_fr = None
total_dollars = 0
for line in fileinput.input():
  (fr, to, to_old, w1, w2, w3, cat, yr, dollar) = line.rstrip().split("\t")
  yr = int(yr)
  if dollar == "N/A":
    dollar = 0
  else:
    dollar = int(dollar.replace(",", "").replace("$", ""))

  if fr != last_fr:
    only = ""
    if last_fr is not None and len(unique_to) == 1:
      only = unique_to.pop()
      unique_to.add(only)

    if (last_fr is not None 
        and total_dollars > 10000
        and "ommunity" not in last_fr
        and "ewish" not in last_fr
        and last_fr not in EXCLUDE
        and only not in ["PROTECT", "FIRE", "EFF"]):

      cols = [
          last_fr,
          str(most_recent),
          str(total_count),
          str(len(unique_to)),
          fmt_dollar(min_dollar),
          fmt_dollar(max_dollar),
          fmt_dollar(new_total_dollars),
          fmt_dollar(old_total_dollars)
      ]

      cols.append(make_summary(new_counts, new_totals))
      cols.append(make_summary(old_counts, old_totals))

      for org in ORGS:
        if all_counts[org] > 0:
          cols.append("{} x {}".format(all_counts[org], org))
          cols.append(fmt_dollar(all_totals[org]))
        else:
          cols.append("")
          cols.append("")

      sort_by = new_total_dollars
      if len(unique_to) == 1:
        sort_by /= 1000.0
      rows.append([sort_by, DELIM.join(cols)])

    last_fr = fr

    total_count = 0
    all_counts = defaultdict(int)
    old_counts = defaultdict(int)
    new_counts = defaultdict(int)

    total_dollars = 0
    old_total_dollars = 0
    new_total_dollars = 0
    all_totals = defaultdict(int)
    old_totals = defaultdict(int)
    new_totals = defaultdict(int)

    unique_to = set()
    most_recent = 0
    min_dollar = 99999999999
    max_dollar = 0

  all_counts[to] += 1
  all_totals[to] += dollar
  if yr < 2016:
    old_counts[to] += 1
    old_totals[to] += dollar
    old_total_dollars += dollar
  else:
    new_counts[to] += 1
    new_totals[to] += dollar
    new_total_dollars += dollar

  total_dollars += dollar
  total_count += 1
  unique_to.add(to)
  most_recent = max(most_recent, yr)
  if (dollar > 0):
    min_dollar = min(min_dollar, dollar)
    max_dollar = max(max_dollar, dollar)

header()
for sort, row in reversed(sorted(rows)):
  print(row)
