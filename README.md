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

## Stuff from the upstream [README.md](https://github.com/cosmicpython/code/blob/master/README.md)

>### Running the tests
>
>```sh
>make test
># or, to run individual test types
>make unit
>make integration
>make e2e
># or, if you have a local virtualenv
>make up
>pytest tests/unit
>pytest tests/integration
>pytest tests/e2e
>```
>
>### Makefile
>
>There are more useful commands in the makefile, have a look and try them out.
