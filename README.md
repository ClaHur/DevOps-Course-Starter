# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Connection to Trello
To connect the app to Trello:

- Create a Trello account and a 'todo' board if you don't have one already
- Create an API Key for Trello. To do this you’ll first need to create a Trello Power Up [from this page](https://trello.com/power-ups/admin)
- After creating a Trello Power Up you’ll be given the option to generate a new API key
- Create an API Token for Trello. This can be done by clicking the “Token” link on the same page where your API key is displayed.

Add you API key, Token, Board ID and list names* into the .env file. You can use the instructions [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call) to find out you Board ID.

NOTE: The app assumes your Trello board has two lists. The first should be the 'todo' list and the second should be the 'done' list. Choose whatever names you like for your lists, so long as they match between Trello and your env file. 

## Tests
To run the automated unit tests:
```bash
$ poetry run pytest
```

## Provisioning a VM from an Ansible Control Node
Ensure the contents of the [ansible](ansible) folder are on the control node. Verify the IP address in the ['inventory'](ansible/inventory) matches the managed node you wish to provision the VM on. 

Run the following command, providing the env variables when prompted:
```bash
$ ansible-playbook playbook.yaml -i inventory
```

## Running the app in a Docker container
### Build the Docker Image:
Use the following command to build the Docker image and tag it as todo-app.

Production:
```bash
$ docker build --target production --tag todo-app:prod .
```

Development:
```bash
$ docker build --target development --tag todo-app:dev .
```

Test:
```bash
$ docker build --target test --tag todo-app:test .
```

### Run the Docker Container:
Run the container using the .env file to set environment variables and map port 5000 of the container to port 5000 on your host machine.

Production:
```bash
$ docker run --env-file .env -p 5000:5000 todo-app:prod 
```

Development (with hot reload - remove mount paramter if unwanted):
```bash
$ docker run --env-file .env -p 5000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/app/todo_app" todo-app:dev
```
Test:
```bash
$ docker run todo-app:test
```

## Deploying the app
### Deploying a new image to Docker Hub
Docker image can be found [here](https://hub.docker.com/r/clahur/todo-app/tags).

1. Log into DockerHub locally, with ```docker login```
2. Build the image, with 
    ```bash
    $ docker build --target production --tag <user_name>/todo-app:prod .
    ```
3. Push the image, with 
    ```bash
    $ docker push <user_name>/todo-app:prod .
    ```

### Updating the container
1. Find the webhook URL in Azure: this can located under Deployment Center on the app service’s page in the Azure portal.
2. Run ```curl -v -X POST '<webhook>'``` in a Linux/Mac shell (or Git Bash on Windows)


