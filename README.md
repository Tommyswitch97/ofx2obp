# Objectives

Populate an Open Bank Project instance with many years of dummy (but valid) transaction data
to help with demos, developer experience, and evaluation.

- Take a valid OFX file [easily generated](https://github.com/chrisjsimpson/fixofx)
- Convert to Open Bank Project [valid import structure](https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/2016-04-28/example_import.json)
- HTTP POST payload to Open Bank Project instance

## Install

```
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```


## Run / Example post to OBP instance

**Note:** For this to work, you must be:

- logged in via the api (e.g. via token login method)
- a 'super admin' (your user id must be in the 'super users' in the props file)

### Convert valid OFX file into valid OBP import payload to stdout
```
python scratch.py -f test.ofx
```
### Convert valid OFX file into valid OBP and post into an OBP instance using curl

The following posts to stdout a valid Open Bank Project payload, which gets inserted into it's database. 

    python scratch.py -f test.ofx 2>/dev/null | curl -d @- -X POST -H "Content-Type: application/json" -H 'Authorization: DirectLogin token="<TOKEN>"' http://localhost:8080/obp/v2.1.0/sandbox/data-import

test.ofx was generated using [fixofx](https://github.com/chrisjsimpson/fixofx#command-line-operation)


Do a call to `/banks` or similar to verify data was added:

    curl -H "Content-Type: application/json" -H 'Authorization: DirectLogin token="<TOKEN>"' http://localhost:8080/obp/v3.0.0/banks 


