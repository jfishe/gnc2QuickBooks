#!/usr/bin/python
import csv

hdr1 = ('!TRNS', 'TRNSID', 'TRNSTYPE', 'DATE', 'ACCNT',
        'NAME', 'AMOUNT', 'DOCNUM', 'MEMO', 'CLEAR')
hdr2 = ('!SPL', 'SPLID', 'TRNSTYPE', 'DATE', 'ACCNT', 'NAME',
        'AMOUNT', 'DOCNUM', 'MEMO', 'CLEAR')

gnchdr = ('Date', 'Account Name', 'Number', 'Description', 'Notes', 'Memo',
          'Category', 'Type', 'Action', 'Reconcile', 'To With Sym',
          'From With Sym', 'To Num.', 'From Num.', 'To Rate/Price',
          'From Rate/Price')

usetrns = dict(Date='DATE', Category='ACCNT', Description='NAME', Number='DOCNUM', Memo='MEMO', Reconcile='CLEAR')

openhdr = '!TRNS'
splhdr = '!SPL'
endhdr = '!ENDTRNS'
endtrns = 'ENDTRNS'
trnstype = 'TRANSFER'


# Add header rows to DictWriter output list
out = []
outrow = {}
for i, key in enumerate(hdr1):
    outrow[str(key)] = hdr1[i]
out.append(outrow)
outrow = {}
for i, key in enumerate(hdr1):
    outrow[str(key)] = hdr2[i]
out.append(outrow)
outrow = {}
outrow[str(openhdr)] = endhdr
out.append(outrow)

with open('Integrity-test2-Liability.csv') as csvinfile:
    reader = csv.DictReader(csvinfile)
    account = ''
    name = ''
    date = ''
    docnum = ''
    transaction = False
    firstrans = True
    split = False
    for row in reader:
        outrow = {}
        for key in usetrns:
            if key in row:
                outrow[usetrns[str(key)]] = row[str(key)]
        if row['Type'] == 'T':
            account = row['Category']
            name = row['Description']
            date = row['Date']
            docnum = row['Number']
            split = True
            transaction = True
            account_name = row['Account Name']
        else:
            outrow['NAME'] = name
            outrow['DATE'] = date
            outrow['DOCNUM'] = docnum
            outrow['TRNSTYPE'] = trnstype
            if row['From Num.']:
                outrow['AMOUNT'] = -float(row['From Num.'].replace(',', ''))
            else:
                outrow['AMOUNT'] = -float(row['To Num.'].replace(',', ''))
        if split is True and row['Type'] == 'S':
            outrow['!TRNS'] = 'TRNS'
            split = False
        else:
            outrow['!TRNS'] = 'SPL'
        if account_name == 'Wells Fargo Credit':
            if row['Type'] == 'S':
                out.append(outrow)
            if transaction is True:
                transaction = False
                if firstrans is False:
                    out.append({str(openhdr): endtrns})
                else:
                    firstrans = False
        else:
            continue
    for row in out:
        if row['!TRNS'] == 'SPL' and row['ACCNT'] == 'Wells Fargo Checking':
            print row
    ifound = False
    for row in out:
        if row['!TRNS'] == 'TRNS' and row['ACCNT'] == 'Wells Fargo Checking':
            ifound = True
            out.remove(row)
        elif ifound is True and row['!TRNS'] == 'SPL':
            out.remove(row)
        else:
            ifound = False
    out.append({str(openhdr): endtrns})

row = {}
with open('test1.csv', 'wb') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=hdr1, dialect='excel-tab')
    for row in out:
        writer.writerow(row)
