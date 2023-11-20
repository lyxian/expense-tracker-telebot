# expense-tracker

Description: This app will store different expenses into MySQL DB for future retrievel

Requirements:

- start DB connection
  - via mysql/mariadb client in dynamic shell script
- DB commands :
  - select
  - insert
  - update
  - delete

RDBMS:

- users
  - num
  - username
  - id (pk)
  - created
- records
  - num (pk)
  - id
  - category
  - amount
  - timestamp
  - created
- categories
  - id
  - category

```
##Packages (list required packages & run .scripts/python-pip.sh)
cryptography==37.0.4
requests==2.28.1
pendulum==2.1.2
flask==2.2.2
pyyaml==6.0
pytest==7.1.2

pyTelegramBotAPI==4.4.0
##Packages
```
