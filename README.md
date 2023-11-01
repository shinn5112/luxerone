# Unofficial Luxer One Python Client

[![MIT License](https://img.shields.io/badge/any_text-liscense-blue)](https://github.com/shinn5112/luxerone/blob/master/LICENSE)
![GitHub release (with filter)](https://img.shields.io/github/v/release/shinn5112/luxerone)
[![PyPI version](https://badge.fury.io/py/luxerone.svg)](https://badge.fury.io/py/luxerone)
![Publish Workflow](https://github.com/shinn5112/luxerone/actions/workflows/python-publish.yaml/badge.svg)
![https://readthedocs.org/projects/luxerone/badge/?version=latest](https://readthedocs.org/projects/luxerone/badge/?version=latest)


An unofficial Python client for the [Luxer One Residential](https://www.luxerone.com/market/residential/) API. 

## Example

```python
from luxerone.client import LuxerOneClient

# credentials
username = "youremail@example.com"
password = "your_password"

# authenticate
luxer_one_client = LuxerOneClient(username, password)
# print all pending packages
pending = luxer_one_client.get_pending_packages()
print(f'Number of pending packages:{len(pending)}')
print("=======================================")
for package in pending:
    print(f'Package id: {package.id}, Locker: {package.locker}, Access Code: {package.accessCode}')

# logout
luxer_one_client.logout()

```

For more details, please see the docs.