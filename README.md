# KeeperBot
Intelligent CLI contact manager.
Allows you to store contact book, notes, tags and additional related information.

| Name | Phone         | Email       | Birthday   | Address         | Notes  | Tag     | Owner |
| ---- | ------------- | ----------- | ---------- | --------------- | ------ | ------- | ----- |
| Me   | +380668009090 | <me@mail.com> | 01.08.2024 | Baker Street, 1 | order  | finance | +     |
| Alex | +380668009091 | <al@mail.com> | 01.08.2023 | Baker Street, 2 | wishes |         | +     |

## Commands and functions

- `hello` - Get a greeting from the bot
- `help` - Displays help for available commands
- `exit` - Exit the program
- `close` - Exit the program
- `add [contact, email, address, birthday, note, tags]` - Add a new contact or add details to an existing contact
  - `contact [name] [phone]` - Add a new contact with a name or replace an existing phone number
  - `email [name] [email]` - Add/replace an email for the specified contact
  - `address [name] [address]` - Add/replace an address for the specified contact
  - `birthday [name] [DD.MM.YYYY]` - Add/replace a birthday for the specified contact
  - `note [contact name]` - Add note for the specified contact
  - `tags [note title]` - Add tag to note
- `edit  [info, phone, note]` - Edit contact information
  - `info [name] [name, birthday, email, address] [new value]` - Edit contact information
  - `phone [name] [old phone] [new phone]` - Edit contact phone number
  - `note [contact name] [note title]` - Edit note by title
- `delete  [contact, phone, info, note, tag]` - Delete contact information
  - `contact contact [name]` - Delete contact
  - `phone [name] [phone]` - Delete contact phone number
  - `info [name] [birthday, email, address]` - Delete contact info
  - `note [contact name] [note title]` - Delete note by title
  - `tag [tag name] [note title]` - Delete tag
- `show  [all, birthday, birthdays, phones, notes]` - Show information about a contact
  - `all` - Show all contacts in the address book
  - `birthday [name]` - Show the birthday for the specified contact
  - `birthdays [days/empty]` - Show birthdays that will occur within the next number of days, empty for today
  - `phones [name]` - Show phones for the specified contact
  - `notes [name]` - Show all notes phones for the specified contact
- `find  [notes-by-tag, notes-by-title]` - Find information about a contact
  - `notes-by-tag` - Find all notes by tag
  - `notes-by-title [note title]` - Find notes by title
- `search-by  [all, name, phone, email, address, birthday, note, tag]` - Search for contacts by field
  - `all [text]` - Search by all fields for all contacts
  - `name [text]` - Search by name for all contacts
  - `phone [phone]` - Search by phone for all contacts
  - `email [email]` - Search by email for all contacts
  - `address [address]` - Search by address for all contacts
  - `birthday [DD.MM.YYYY]` - Search by birthday for all contacts
  - `note [note title]` - Search by note for all contacts
  - `tag [tag name]` - Search by tag for all contacts

## KeeperTeam

- <nickolasz@gmail.com>
- <eugenkhudoliiv@gmail.com>
- <brelyk09@gmail.com>
- <viacheslavpaterov@gmail.com>
- <andriyberzerk@gmail.com>
- <viacheslavpaterov@gmail.com>

## Resources
- Repo: [https://github.com/yourusername/KeeperBot](https://github.com/yourusername/KeeperBot)
- Trello: [KeeperTeam](https://trello.com/invite/b/66ba58163e0e996c03a43233/ATTI3c43b36eb8846e95058a58bced7b0c5f101A71A0/team-10)
- Slack: [KeeperTeam](https://app.slack.com/client/T06BSG8A6VA/C07GWBN88Q1)


## Module Build

Before building and installing the module using the command `pip list | grep wheel`, make sure that `wheel` is installed on your system.

Next, perform the build:

```
cd root KeeperBot project folder
python setup.py sdist bdist_wheel
pip install .
```
or install your package in editable mode
```
pip install -e .
```
## Generating Dependency List

- Creating the list: `pip freeze > requirements.txt`
- Installing dependencies: `pip install -r requirements.txt`
