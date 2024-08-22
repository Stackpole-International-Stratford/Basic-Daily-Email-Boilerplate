# Basic Daily Email Boilerplate

requires a .env file with the following variables:
# Database credentials
DB_PASSWORD=
DB_USER=
DB_HOST=10.4.1.224
DB_PORT=3306
DB_NAME=prodrptdb

# Email server details
EMAIL_SERVER=smtp01.stackpole.ca
EMAIL_FROM=tyler.careless@johnsonelectric.com
EMAIL_SUBJECT=
EMAIL_LIST=




requires a report function that returns the report body in HTML
currently using Jinja2 templates.

## Usage

Fork this repo giving it a meaningful name

Clone:

`git clone https://github.com/Stackpole-International-Stratford/<your forked repo>.git`

or update with:

`git pull`

build with:

`docker compose build`

run with:

`docker compose up` 


