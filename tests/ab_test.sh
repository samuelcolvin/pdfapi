#!/bin/sh
ab -n 20 -c 10 -p tests/test.html http://localhost:5000/create
