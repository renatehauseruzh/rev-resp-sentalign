#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..

data=$base/data

mkdir -p $data

#tools=$base/tools

# isolate test data
csvgrep -c split -m "test" $data/trip_hotels.csv > $data/trip_hotels_test.csv

# randomly sample 1000 review-response pairs from the test data
shuf -n 1000 $data/trip_hotels_test.csv > $data/trip_hotels_test_1000_rand.csv
