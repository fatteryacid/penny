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
`process_colname()` takes one parameter: **dataframe**.
- Removes whitespace from column names.
- Returns updated dataframe with cleaned column names.

`process_string()` takes one parameter: **dataframe** and one optional parameter: **column_list**.
- Removes whitespace from all rows based on columns passed through it.
- If nothing is passed for column_list, it will return the same dataframe.
- Returns updated dataframe.

`process_distribution()` takes one parameter: **dataframe** and one optional parameter: **column_list**.
- Ensures distribution values will be cast as integers and not floats.
- If nothing is passed for column_list, it will return the same dataframe.
- Returns updated dataframe.

`process_amount()` takes no parameters.
- Removes all special characters from amount column.
- Converts accounting-formatted negative currency values to traditional negative values.
- Returns updated dataframe.

`process_ignore()` takes one parameter: **dataframe** and one optional parameter: **ignore_list**.
- Removes ignored columns based on ignore_list.
- If nothing is passed for ignore_list, it will return the same dataframe.
- Returns updated dataframe.

`trunc_df()` takes one parameter: **dataframe** and one optional parameter: **latest_id**.
- Removes all data on top of **latest_id**. Used to crop dataframe to only return new values.
- If nothing is passed for latest_id, it will return the same dataframe.
- Returns updated dataframe.

`format_labels()` takes one parameter: **dataframe** and one optional parameter: **column_list**.
- Formats special characters to be more machine-readable.
- If nothing is passed for column_list, it will return the same dataframe.
- Returns updated dataframe.

### load.py
`select_from()` takes two parameters: **engine_url** and **table_object**.
- Returns a list of tuples mimicking a SQL SELECT query.

`insert_into()` takes three parameters: **engine_url**, **table_object** and **value_list**.
- Sends a list of dictionaries to mimic an INSERT INTO .. VALUES.
- If data tries to create duplicates, function will skip.