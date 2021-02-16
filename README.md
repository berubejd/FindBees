# Find Bees

This is a small Flask app utilizing which is meant to pair up people from a group for weekly activities such as team building exercises.

For "database" access, this project also includes:

- [gspread](https://gspread.readthedocs.io/)

The simple layout utilizes [Bootstrap 4](https://getbootstrap.com/).

## Screenshot

### Landing page

![Landing Screenshot](images/landing.png?raw-true)

## Configuration

The configuration for this application can be done through a .env file.  An example of that file is included.  At a minimum you will need to update:

- SECRET_KEY
- WORKSHEET_NAME
- WORKSHEET_SECRETS_FILE

In order to access Google Spreadsheets you will need to provide an appropriate service_account.json file.  Directions can be found [here](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account).

The initial spreadsheet will require a single column with a header labeled 'Name' and the list of users below in column 1:

|Name|
|---|
|John|
|Mary|
|...|
