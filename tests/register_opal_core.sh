#!/usr/bin/env bash


#curl 'http://localhost:5000/client/' \
#    -X POST -kv \
#    -H 'Content-Type: application/json' \
#    -H 'Origin: http://localhost:8085' \
#    -H 'Cookie: i18next=en; oidc_id_token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxMzk3MDgyMSwiZXhwIjoxNTEzOTc0NDIxfQ.eyJzdWIiOiI5MDM0Mi5BU0RGSldGQSIsImF1ZCI6IjdjMmMwNzcxLTEzMWUtNGViYy05OTE0LTk1ZTQ4ZGZjOWRmMiIsImF1dGhfdGltZSI6MTUxMzk2NzA5Nywia2lkIjoicnNhMSIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4NS9vcGVuaWQtY29ubmVjdC1zZXJ2ZXItd2ViYXBwLyIsImV4cCI6MTUxMzk3MTQyMSwiaWF0IjoxNTEzOTcwODIxLCJqdGkiOiIxNzUyYjI4Mi0wYzljLTQwNGEtYmExNi1iNTE3ZjNhMjYyZjgifQ.sWZWFVAJ0ZXAjY1PiPTxVlC_CZ6ICmSbhpc0oG6dBnQ' \
#    --data-binary @register_opal_core.json

curl 'http://localhost:5000/client/2' \
    -X DELETE -kv \
    -H 'Content-Type: application/json' \
    -H 'Origin: http://localhost:8085' \
    -H 'Cookie: i18next=en; oidc_id_token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxMzk3MDgyMSwiZXhwIjoxNTEzOTc0NDIxfQ.eyJzdWIiOiI5MDM0Mi5BU0RGSldGQSIsImF1ZCI6IjdjMmMwNzcxLTEzMWUtNGViYy05OTE0LTk1ZTQ4ZGZjOWRmMiIsImF1dGhfdGltZSI6MTUxMzk2NzA5Nywia2lkIjoicnNhMSIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4NS9vcGVuaWQtY29ubmVjdC1zZXJ2ZXItd2ViYXBwLyIsImV4cCI6MTUxMzk3MTQyMSwiaWF0IjoxNTEzOTcwODIxLCJqdGkiOiIxNzUyYjI4Mi0wYzljLTQwNGEtYmExNi1iNTE3ZjNhMjYyZjgifQ.sWZWFVAJ0ZXAjY1PiPTxVlC_CZ6ICmSbhpc0oG6dBnQ'


