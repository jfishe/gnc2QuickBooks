#!/usr/bin/python
import csv

__author__ = 'jfisher'

QB_accounts = []
with open('Book2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        QB_accounts.append(row['Account'])

gnc_accounts = []
with open('liability.iif') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel-tab')
    for row in reader:
        gnc_accounts.append(row['ACCNT'])
with open('bank.iif') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel-tab')
    for row in reader:
        gnc_accounts.append(row['ACCNT'])

gnc_accounts = list(set(gnc_accounts))
gnc_diff = []
for item in QB_accounts:
    if item not in gnc_accounts:
        gnc_diff.append(item)
gnc_diff = set(gnc_diff)
for item in gnc_diff:
    print(item)
