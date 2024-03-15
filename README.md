# FORD - Security vulnerabilities fixer

## Dependencies

- Python 3.11.x
- Linux or MacOS

## Env Configuration

Duplicate the file ".env.secrets_and_paths.template" to the same directory, rename to ".env.secrets_and_paths"
Open the file and change the values (doc inside it)

## Installation

Create a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```sh
make deps
```

# Run application

Help
```sh
python3 src/app.py --help
```

Start the API server (swagger at http://127.0.0.1:8000/docs)
```sh
python3 src/app.py --api-server
```

Command line example to run security fixer
```sh
python3 src/app.py --entrypoint_folder="Wings" --security_tool="42crunch" 
```
