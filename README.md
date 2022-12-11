# Financial ETL Process
*Version 1.0.0.1*


Moves and models date from Google Sheets to a local PostgreSQL database.
Data is modeled with dimensional modeling practices.


# What's new for Version 1.0.0.1
* Moved away from `gspread` as a dependency. Now uses Google Sheets API directly.
    - With this comes need for OAuth usage. Will open a Google Authentication webpage on: `localhost:5537`.
* Moved away from ETL paradigm to ELT paradigm.
    - Workflow: GoogleSheets > Pandas > dbt
    - Users can add new models to `penny/app/dbt/penny/model/`. All models must reference `fact` relation by using: `{{ ref('fact') }}`.
    - SQLAlchemy is no longer the method of insertion to database. Instead, uses SQLAlchemy under the hood through Pandas.
* Airflow support provided with `airflow_dag.py`.



## Planned Changes
1. Dockerize with `Airflow` to write to external database.
2. Clean up `/penny/app/dbt/penny` directories.
3. Reorganize all configuration files.
