#!/bin/sh
echo "Initializing staging environment"

dropdb penny_stg 
createdb penny_stg

for filename in ./sql/*.sql; do
    psql -d penny_stg -f $filename
done

echo "New staging environment established. Connect using 'psql -d penny_stg'"

