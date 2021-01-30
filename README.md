# Find Bees

This is a small Flask app utilizing which is meant to pair up people from a group for weekly activities such as team building exercises.

For "database" access, this project also includes:

- [gspread](https://gspread.readthedocs.io/)

The simple layout utilizes [Bootstrap 4](https://getbootstrap.com/).

## Screenshot

### Landing page

![Landing Screenshot](images/landing.png?raw-true)

## Configuration

At a minimum, you will probably want to set:

- FLASK_APP = name (This should match what the 'application' directory is renamed to.)
- FLASK_ENV = development (If you would like the app to provide log output and autoreload.)

In order to access Google Spreadsheets you will need to provide an appropriate service_account.json file.  Directions can be found [here](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account).
