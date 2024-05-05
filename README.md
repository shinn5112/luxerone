# Unofficial Luxer One Python Client

![GitHub release](https://img.shields.io/github/v/release/shinn5112/luxerone?sort=semver&color=blue)
[![PyPI version](https://badge.fury.io/py/luxerone.svg)](https://badge.fury.io/py/luxerone)
[![MIT License](https://img.shields.io/badge/liscense-MIT-blue)](https://github.com/shinn5112/luxerone/blob/master/LICENSE)

![https://readthedocs.org/projects/luxerone/badge/?version=latest](https://readthedocs.org/projects/luxerone/badge/?version=latest)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Imports: isort](https://img.shields.io/badge/imports-isort-blue)](https://pycqa.github.io/isort/)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=shinn5112_luxerone)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=shinn5112_luxerone&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=shinn5112_luxerone)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=shinn5112_luxerone&metric=bugs)](https://sonarcloud.io/summary/new_code?id=shinn5112_luxerone)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=shinn5112_luxerone&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=shinn5112_luxerone)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=shinn5112_luxerone&metric=coverage)](https://sonarcloud.io/summary/new_code?id=shinn5112_luxerone)


![Publish Workflow](https://github.com/shinn5112/luxerone/actions/workflows/verification.yaml/badge.svg)
![Publish Workflow](https://github.com/shinn5112/luxerone/actions/workflows/python-publish.yaml/badge.svg)


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

For more details, please see the [docs](https://luxerone.readthedocs.io/en/latest/).
