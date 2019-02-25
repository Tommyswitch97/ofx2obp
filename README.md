# Objectives

Populate an Open Bank Project instance with many years of dummy (but valid) transaction data
to help with demos, developer experience, and evaluation.

- Take a valid OFX file [easily generated](https://github.com/chrisjsimpson/fixofx)
- Convert to Open Bank Project [valid import structure](https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/2016-04-28/example_import.json)
- HTTP POST payload to Open Bank Project instance

## Example post

**Note:** For this to work, you must be:

- logged in via the api (e.g. via token login method)
- a 'super admin' (your user id must be in the 'super users' in the props file)

The following posts to stdout a valid Open Bank Project payload, which gets inserted into it's database. 

    python scratch.py -f test.txt 2>/dev/null | curl -d @- -X POST -H "Content-Type: application/json" -H 'Authorization: DirectLogin token="<TOKEN>"' http://localhost:8080/obp/v2.1.0/sandbox/data-import

Do a call to `/banks` or similar to verify data was added:

    curl -H "Content-Type: application/json" -H 'Authorization: DirectLogin token="<TOKEN>"' http://localhost:8080/obp/v3.0.0/banks 


