# Financial ETL Process
Moves and models date from Google Sheets to a local PostgreSQL database.
Data is modeled with dimensional modeling practices.


## Installation
Application should install dependencies by itself upon calling:
```
bash run.sh
```


However, certain `gspread` may not be properly configured in terms of using Google Service Accounts.
Please refer to the [official GSpread documentation](https://docs.gspread.org/en/latest/oauth2.html#service-account) for installation instructions.

For further information on dependencies, please read requirements.txt.


## Usage
To make the most out of `penny`, use `cron` to schedule `bash /YOUR_DIRECTORY/run.sh` to run on a weekly schedule.
Alternatively, you can manually run `bash/YOUR_DIRECTORY/run.sh`


## Future Changes
* Convert to object-oriented design to instantiate table objects
* Convert from using SQLAlchemy CORE to ORM
* Add orchestration, possibly with AirFlow
