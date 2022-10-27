#!/bin/sh
dropdb penny
createdb penny

for filename in ./sql/*.sql; do
    psql -d penny -f $filename
done

