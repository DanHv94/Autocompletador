# Project Structure

The project is structured based on the Repository and the Dependency Injection Patterns.

```
API/
    contexts/                               // Database contexts
    controllers/                            // Endpoint definitions
    interfaces/                             // Interfaces to connect to databases
    models/                                 // Pydantic models
    repositories/                           // Repositories that uses interfaces
    services/                               // Services
    .gitignore                              // Ignore files for Git
    config.py                               // File that loads the env vars
    main.py                                 // Server manager
    README.md                               // Instructions file
    requirements.txt                        // Requirements for the application
```

<div style="margin-bottom: 3%"></div>

# Requirements

For this project you need the next requirements

* Python >= 3.8
* pip >= 19.0.2
* virtualenv or pyenv

Then you have to create a virtual environment

* With virtualenv:

  ```console
  $ virtualenv -p python3 venv

  $ source venv/bin/activate

  $ pip install -r requirements.txt
  ```

* With pyenv:
  ```console
  $ pyenv virtualenv 3.8.x venv

  $ pyenv activate venv

  $ pip install -r requirements.txt
  ```
<div style="margin-bottom: 3%"></div>

# Local Environment
## Set DB

This application is designed to consume data from a MongoDB database called *AbInBev*. 

Data (you can download it from <a href="https://drive.google.com/file/d/1ji0zSzBrQQjSphPuL7_rJQNtgs94uEJG/" class="external-link" target="_blank">https://drive.google.com/file/d/1ji0zSzBrQQjSphPuL7_rJQNtgs94uEJG/</a>) should be loaded into a collection called *cities*

## Run the API

To run the API use the following code:
    ```console
    $ ENV=dev uvicorn main:app --reload --port 3001

    INFO:     Uvicorn running on http://127.0.0.1:3001 (Press CTRL+C to quit)
    INFO:     Started reloader process [28720]
    INFO:     Started server process [28722]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

<div style="margin-bottom: 3%"></div>


# Documentation

Because the API is built using FastAPI, the documentation for the endpoints is built automatically.

## OpenAPI

Previously known as Swagger UI, to access the interactive docs open your browser at <a href="http://127.0.0.1:3001/docs" class="external-link" target="_blank">http://localhost:3001/docs</a>.

Using this platform, you can test the endpoint.