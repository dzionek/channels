# Channels

Flask web-application where you can create own channels, manage them, and chat with your friends/colleagues.
Created with Python, TypeScript, SCSS, Bootstrap, Socket.io, Handlebars templates, and love. Bundled with Webpack.
Containerized with Docker.

Inspired by the Project 2 of Harvard's [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2018/).

## Usage

### 1) Preferable way – with Docker

Install [Docker](https://www.docker.com/get-started), build the container, and run it.

```bash
docker-compose up -d --build
```

Your website should be available at [localhost:5000](localhost:5000).

### 2) Without Docker
* If you don't want to use Docker, change the directory to *web*.

    ```bash
    cd web
    ```

* **Optional:** If you wish to separate these python packages from your global ones,
create a virtual environment with [pip](https://pip.pypa.io/en/stable/).

    ```bash
    python -m pip install --upgrade pip
    pip install virutalenv
    virtualenv venv
    source venv/bin/activate  # for Linux/MacOS, on Windows do instead: venv\Scripts\activate
    ```

* Use Python package manager [pip](https://pip.pypa.io/en/stable/) and Node.JS package manager [npm](https://nodejs.org) to install the requirements.

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    npm install --save
    npm run build
    ```

* Create [PostgreSQL](https://www.postgresql.org) database. Then, create environmental variables *DATABASE_URI*
with the address of that database. Also, set environmental variable *SECRET_KEY* used for administering the app.

    * Linux/MacOS:
    
        ```bash
        export DATABASE_URI=postgres://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB NAME}
        export SECRET_KEY={YOUR SECRET KEY}
        ```

    * Windows:
    
        ```cmd
        set DATABASE_URI=postgres://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB NAME}
        set SECRET_KEY={YOUR SECRET KEY}
        ```

* Create the necessary databases.

    ```bash
    python manage.py create-db
    ```

* Run the app. Your application should be at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

    ```bash
    python manage.py run
    ```

## TODO:
**Login and Registration**
- [x] Better main page
- [x] Registration view
- [ ] Sending email and confirming
- [ ] Forget password

**Functionality**
- [x] Channels should have passwords
  - [x] Join a channel modal
  - [x] Add password to channel model
  - [x] Leave a channel
- [ ] REST API
- [ ] Refactor and use more OOP

**Design**
- [ ] Black mode

**Learn and Use**
- [x] Docker container
- [ ] More unit tests
- [ ] Add Travis CI
- [ ] Deploy to AWS/Heroku
