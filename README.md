# google-finance-page-selenium-python
project with using selenium python simple page object model framework and running tests in github actions successfully
# FINFARE TAKE HOME EXERCISE #

The simple folder structure looks like - 
```
google-finance-page-selenium-python/
.github/
├─ workflows/
│  ├─ main.yml
src/
├─ pages/
│  ├─ google_finance_home_page.py
test/
├─ test_google_finance_home_page.py
README.md
requirement.txt
```


Run Test:
Tests can be run for now on Chrome
```
pytest -v -s
pytest -v -k test_only_in_retrieved_symbols
```


