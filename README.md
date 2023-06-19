# Airflow-example-etl and NIFI for windows docker

## Getting Started

These instructions will get you a copy of the project up and running it on your local Windows machine for development and testing purposes.

- Install the prerequisites
- Clone this repo
```
git clone https://github.com/Raul-dev/Airflow-example-etl.git
cd Airflow-example-etl
```
- Run the bath file from PowerShell
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
./start.ps1
```
- Check https://localhost User: airflow, Password: airflow  (or http://localhost:8080 if SSL disabled)
- Done! :tada:

### Run this pipline first:
- 003_plsql_insert
- 010_plsql_init_connection
- 040_oracle_init_connection
### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Install [Win64OpenSSL](https://slproweb.com/download/Win64OpenSSL-3_1_1.msi)
- Add ENV Variable for running openssl.exe: Path=Path:C:\Program Files\OpenSSL-Win64\bin
- Install (optional) [Powershell 7.3](https://github.com/PowerShell/PowerShell/releases/download/v7.3.4/PowerShell-7.3.4-win-x64.msi)
- Following the Airflow 2.6.1 release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)


#### Code used from other repositories:

#### piplines 011-016
- ETL Best practices with airflow repository.
https://gtoonstra.github.io/etl-with-airflow/
https://github.com/gtoonstra/etl-with-airflow




