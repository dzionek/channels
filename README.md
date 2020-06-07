# Channels

Flask web-application where you can create own channels and chat with your friends/colleagues. Created with Python, TypeScript, SCSS, Bootstrap, Socket.io, Handlebars templates, and love. Bundled with Webpack.

Inspired by the Project 2 of Harvard's [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2018/).

## Installation

**Optional:** If you wish to separate this python packages from your global ones, create a virtual environment and then follow the instruction below.
```bash
python -m pip install --upgrade pip
pip install virutalenv
virtualenv venv
source venv/bin/activate
```

Use the Python's package manager [pip](https://pip.pypa.io/en/stable/) and Node.JS package manager [npm](https://nodejs.org) to install the requirements.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
npm install --save
npm run build
```

Create [PostgreSQL](https://www.postgresql.org) database and save your DATABASE_URI in *secrets.py* along with your SECRET_KEY for administering the app.

```bash
echo 'DATABASE_URI = "postgres://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB NAME}"' >> secrets.py
echo 'SECRET_KEY = "{YOUR SECRET KEY}"' >> secrets.py
```

## Run
Run the setup file in the main directory
```bash
python setup.py
```

## TODO:
**Login and Registration**
- [x] Better main page
- [x] Registration view
- [ ] Sending email and confirming
- [ ] Forget password

**Functionality**
- [ ] Channels should have passwords
  - [ ] Join a channel modal
  - [ ] Add password to channel model
  - [ ] Leave a channel
- [ ] REST API
  - [ ] Refactor and use more OOP

**Design**
- [ ] Message should have own colorful interactive div that changes on hover
- [ ] Black mode
- [ ] More informative top bar
