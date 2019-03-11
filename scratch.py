import os
import io
import sys
import uuid
import json
from optparse import OptionParser
from ofxparse import OfxParser

__doc__ = \
"""Convert a valid OFX 2.0 data into a valid Open Bank Project 
import json payload. Reads either from file, or from stdin.
"""

dummyEmail = ''.join([str(uuid.uuid4()), '@example.com'])

dummyBank = {
                'website': 'https://www.example.com',
                'logo': 'https://static.openbankproject.com/images/sandbox/bank_x.png',
                'id':'psd201-bank-y--uk',
                'short_name': 'Bank Z', 
                'full_name':'The Bank of Y'
        
            }

dummyAccount = {
                'owners': ['robert.yuk.y@example.com'],
                'generate_auditors_view': True,
                'number': '13759969699',
                'label': 'Robert XUk X - M35 ..699',
                'IBAN':  'BA12 1234 5123 4513 7599 6969 977',
                'generate_public_view': False,
                'generate_accountants_view': True,
                'balance': {'currency' : 'GBP',
                            'amount': '8084.32'},
                'type': 'CURRENT PLUS',
                'id': '05237266-b334-4704-a087-5b460a2ecf04',
                'bank': 'psd201-bank-y--uk'
               }

dummyUser = {
        'display_name': dummyEmail[0:32],
        'password': '5232e7',
        'user_name': dummyEmail[0:32],
        'email': dummyEmail
}

dummyTransaction = {
    'id': 'b52a3465-d484-4b9a-97da-308188af7c6a',
    'counterparty': { 'name': 'British Gas' },
    'this_account': { 'id': '05237266-b334-4704-a087-5b460a2ecf04',
                      'bank': 'psd201-bank-y--uk'
                    
    },
    'details': {
        'description': 'Gas/Elec',
        'completed': '2015-07-01T00:00:00.000Z',
        'value': '-114.55',
        'new_balance': '114.55',
        'type': '10219',
        'posted': '2015-07-01T00:00:00.000Z'
    }
}

def convert(text):
    fp = io.StringIO(unicode(rawtext))
    # Parse OFX
    ofx = OfxParser.parse(fp)
    account = ofx.account
    institution = account.institution
    statement = account.statement
    transactions = statement.transactions

    # Build bank object
    bankObj = {
        'website' : 'https://example.com',
        'logo' : 'https://static.openbankproject.com/images/sandbox/bank_x.png',
        'id' : institution.organization,
        'short_name' : institution.organization,
        'full_name' : institution.organization
    }
    # Build account object
    accountObj = {
        'owners': [dummyEmail[0:32]],
        'generate_auditors_view': True,
        'number': account.number,
        'label': account.account_type,
        'IBAN':  account.routing_number, #Wrong
        'generate_public_view': False,
        'generate_accountants_view': True,
        'balance': {'currency' : account.curdef,
                    'amount': float(statement.balance)},
        'type': account.account_type,
        'id': account.account_id,
        'bank': institution.organization
    }

    # Build transaction object
    transactionsObj = [] # list of transactions
    for transaction in transactions:
        try:
            transactionId = transaction.id
        except AttributeError:
            transactionId = ''
        try: 
            payee = transaction.payee
        except AttributeError:
            payee = ''
        try: 
            amount = transaction.amount
        except AttributeError:
            amount = 0
        try:
            transactionType = transaction.type
        except AttributeError:
            transactionType = ''

        transactionObj = {
            'id': transactionId,
            'counterparty': { 'name': payee },
            'this_account': { 'id': account.account_id,
                              'bank': institution.organization
                            
            },
            'details': {
                'description': payee,
                'completed': '2015-07-01T00:00:00.000Z',
                'value': float(amount),
                'new_balance': '114.55', #Wrong
                'type': transactionType,
                'posted': '2015-07-01T00:00:00.000Z'
            }
        }
        transactionsObj.append(transactionObj)


    payload = {'banks': [bankObj], 'accounts': [accountObj], 
                    'users': [dummyUser], 'transactions': [transactionObj]}

    print json.dumps(transactionsObj)



parser = OptionParser(description=__doc__)
parser.add_option("-f", "--file", dest="filename", default=None,
                  help="source file to convert (writes to STDOUT)")
(options, args) = parser.parse_args()

#
# Load up the raw text to be converted.
#
if options.filename:
    if os.path.isfile(options.filename):
        try:
            srcfile = open(options.filename, 'rU')
            rawtext = srcfile.read()
            srcfile.close()
        except StandardError, detail:
            print "Exception during file read:\n%s" % detail
            print "Exiting."
            sys.stderr.write("ofx2obp failed with error code 1\n")
            sys.exit(1)
else:
    stdin_universal = os.fdopen(os.dup(sys.stdin.fileno()), "rU")
    rawtext = stdin_universal.read()
    print "No input.  Pipe a file to convert to the script,\n" + \
          "or call with -f. " 
    sys.stderr.write("ofx2obp failed with error code 3\n")
    sys.exit(3)

#
# Convert the raw text to Open Bank Project (OBP) json import format.
# 
try:
    converted = convert(rawtext)
except StandardError, detail:
    print "Exception during file read:\n%s" % detail
    print "Exiting."
    sys.stderr.write("ofx2obp failed with error code 1\n")
    sys.exit(1)
