#!/bin/sh
dropdb penny
createdb penny

for filename in ./sql/*.sql; do
    psql -d penny_stg -f $filename
done

