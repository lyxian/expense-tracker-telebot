# expense-tracker

Description: This app will store different expenses into MySQL DB for future retrievel

TODO:

- .

Requirements:

- start DB connection
  - via mysql/mariadb client in dynamic shell script
- DB commands :
  - select
  - insert
  - update
  - delete
- App (telebot) :
  - commands (\* = auto-generated)
    - /start,help
    - /join
      - add user to DB << username\*, id\*
    - /add
      - add record to DB << id\*, date, category, amount, comment
    - /edit
    - /query
- CLI :
  - sql queries

RDBMS:

- users
  - num (pk)
  - username
  - id (fk)
  - created
- records
  - num (pk)
  - id (fk)
  - category (fk)
  - amount
  - comment
  - timestamp
  - created
- categories
  - id (pk)
  - category
- statuses
  - id
  - status
- messages
  - num (pk)
  - id (fk)
  - status
  - message
  - lastCallbackId
  - lastUpdated

Issues

- is varchar(50) enough for messages.message AND records.comment?
- query returns text not optimized for viewing
  > sends as image instead using PIL
- .

Done

- add undo to return to previous status
- add undo/cancel for all stages
- db add showTable
- add yesterday for date
- include investment,others in CATEGORIES

```
##Packages (list required packages & run .scripts/python-pip.sh)
cryptography==37.0.4
requests==2.28.1
pendulum==2.1.2
flask==2.2.2
Werkzeug==2.2.2
pyyaml==6.0
pytest==7.1.2

pyTelegramBotAPI==4.4.0
Pillow==10.1.0
##Packages
```
