import os
import io
import sys
import json
from optparse import OptionParser
from ofxparse import OfxParser

__doc__ = \
"""Convert a valid OFX 2.0 data into a valid Open Bank Project 
import json payload. Reads either from file, or from stdin.
"""

dummyBank = {'bank': 
                {
                'website': 'https://www.example.com',
                'logo': '',
                'id':'psd201-bank-x--uk',
                'short_name': 'Bank X', 
                'full_name':'The Bank of X'
        
                }
    }

dummyAccount = {
                'owners': ['robert.xuk.x@example.com'],
                'generate_auditors_view': True,
                'number': '13759969699',
                'label': 'Robert XUk X - M35 ..699',
                'IBAN':  'BA12 1234 5123 4513 7599 6969 977',
                'generate_public_view': false,
                'generate_accountants_view': true,
                'balance': {'currency' : 'GBP',
                            'amount': '8084.32'},
                'type': 'CURRENT PLUS',
                'id': '05237266-b334-4704-a087-5b460a2ecf04',
                'bank': 'psd201-bank-x--uk'
               }

def convert(text):
    fp = io.StringIO(unicode(rawtext))
    # Parse OFX
    parsed = OfxParser.parse(fp)
    pass

#f = open('dummy.json')
#raw = f.read()

#data = json.loads(raw)
#print data.keys()


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
