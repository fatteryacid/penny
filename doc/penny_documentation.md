# penny Documentation

## Understanding Directory Layout
`./diagram` contains drawio.app diagrams and exported SVG files.
`./penny` contains main executable files.
`./setup` contains a subfolder `./setup/sql` which stores all of the SQL scripts used to create empty tables, and `init_sql.sh` and `setup.py` which are run on first startups.
`./tests/` contains a subfolder `./tests/sql` which stores SQL scripts that are used to create a staging environment. This is initialized by running `bash create_stage_environment.sh`.


## Configuration Files Explained
`./penny/config` directory contains configuration for the different connections.
- `db_conf.json` holds schema and prefill data.
- `gs_conf.json` holds Google Sheet schema and metadata.
- `save.json` holds the save state for penny to use from previous runs.


## Main Operations Explained
### extract.py
`get_data()` takes two parameters: **sheet_id** and **ws_loc** which are located directly in `gs_conf.json`.
- Pulls a copy of data from Google Sheets and creates a `Pandas` dataframe. 
- Writes a raw backup of data in CSV format to `./log`

### transform.py
