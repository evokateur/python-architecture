# Code Along: Architecture Patterns with Python

The default branch, `main`, was created from the upstream
[`start`](https://github.com/cosmicpython/code/releases/tag/start) tag.

## Chapters Completed

### I. Building Architecture to Support Domain Modeling

- [x] 1. [Domain Modeling](https://github.com/evokateur/python-architecture/pull/1/files)

- [x] 2. [Repository Pattern](https://github.com/evokateur/python-architecture/pull/2/files)

- [x] 3. [*On Coupling and Abstractions*](https://github.com/evokateur/python-architecture/pull/3/files)

- [x] 4. [API and Service Layer](https://github.com/evokateur/python-architecture/pull/4/files)

- [x] 5. [*TDD in High and Low Gear*](https://github.com/evokateur/python-architecture/pull/5/files)

- [x] 6. [Unit of Work Pattern](https://github.com/evokateur/python-architecture/pull/10/files)

- [ ] 7. Aggregates and Consistency Boundaries

### II. Event-Driven Architecture

- [ ] 8. Events and the Message Bus

- [ ] 9. *Going to Town on the Message Bus*

- [ ] 10. Commands and Command Handler

- [ ] 11. Using Events to Integrate Microservices

- [ ] 12. Command-Query Responsibility Separation

- [ ] 13. Dependency Injection

## Getting Started

### Clone and set up the project

```sh
git clone git@github.com:evokateur/python-architecture.git
cd python-architecture
pyenv shell 3.12
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file based on `.env.example`:

```sh
cp .env.example .env
```

Then edit `.env` and set your Railway PostgreSQL connection string:

```bash
POSTGRES_URI=postgresql://user:password@host:port/database
```

Other important settings in `.env`:
- `FLASK_RUN_PORT=5005` (default port for local Flask)
- `FLASK_APP=entrypoints/flask_app.py`
- `FLASK_ENV=development`

### Add [semi-upstream](https://github.com/evokateur/python-architecture-code)† remote for reference

† a fork I will test the chapter branches in, but not code along in

```sh
git remote add upstream git@github.com:evokateur/python-architecture-code.git
git fetch upstream
```

#### Finding the upstream branches for a chapter

```sh
git branch -r -l 'upstream/chapter_07*'
```

## Development Workflow

### Running the Flask API

Start the Flask development server (connects to Railway PostgreSQL):

```sh
make flask
```

Stop the Flask server:

```sh
make unflask
```

Check Flask logs:

```sh
cat flask.log
```

### Running tests

```sh
# Run all tests
make test

# Run specific test types
pytest tests/unit --tb=short
pytest tests/integration --tb=short
pytest tests/e2e --tb=short

# Watch tests during development
make watch-tests
```

### Code formatting

```sh
make black
```

### Other useful commands

See the `Makefile` for additional commands. Docker Compose is available (`make up`, `make down`) but not used for local development.
