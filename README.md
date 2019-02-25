# Objectives

Populate an Open Bank Project instance with many years of dummy (but valid) transaction data
to help with demos, developer experience, and evaluation.

- Take a valid OFX file [easily generated](https://github.com/chrisjsimpson/fixofx)
- Convert to Open Bank Project [valid import structure](https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/2016-04-28/example_import.json)
- HTTP POST payload to Open Bank Project instance
