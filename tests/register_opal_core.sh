#!/usr/bin/env bash


curl 'http://localhost:5000/client/' \
   -X POST -kv \
   -H 'Content-Type: application/json' \
   -H 'Origin: http://localhost:8085' \
   -H 'Authorization: Bearer eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJhZG1pbiIsImF6cCI6IjA5OGMzMmUwLWE0YmYtNDdhNi1hZTM3LWQ5NWIzZTE5NTg1NSIsImlzcyI6Imh0dHA6XC9cL2xvY2FsaG9zdDo4MDgwXC9vcGVuaWQtY29ubmVjdC1zZXJ2ZXItd2ViYXBwXC8iLCJleHAiOjE1MjAzNTM3MzAsImlhdCI6MTUyMDM1MDEzMCwianRpIjoiYjc3ODkwMjItYmUyZi00MWVlLWFlM2EtZjRlNDMwYWNmNDE5In0.L-Brko5uzde8N-TUwPnghbttW1ekpNXVa64gclWyR1U8R9l0oTN7uXbu1JkIki6VgYTmhWk32hRHFMb7tn9IHQlBHHbr2Rsw01DKB9OZNPrCRJjpaQF_z-bkxJ_MCGxmSY5eTzBeEorLf36kGnZ-er0nJK_3DG6lEeaxdjz1y6ra7JVn3g7KH5Y2XqxCZEGKDRjZVcPzw8DD9uYuUpOK1I2h6Ay1cWcnLJXrenh42XQLdexZC9Rvc1PRXTN-cLoapP7j9WMIWRcjTQT4qGemQDCMr57BRUKnB59IAnbZ-RFwaMEQj--fB_9yLbBexIFUUGmog50RB9nDB8OwdxbUhg' \
   --data-binary @register_opal_core.json

# curl 'http://localhost:5000/client/2' \
#     -X DELETE -kv \
#     -H 'Content-Type: application/json' \
#     -H 'Origin: http://localhost:8085' \
#     -H 'Cookie: i18next=en; oidc_id_token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxMzk3MDgyMSwiZXhwIjoxNTEzOTc0NDIxfQ.eyJzdWIiOiI5MDM0Mi5BU0RGSldGQSIsImF1ZCI6IjdjMmMwNzcxLTEzMWUtNGViYy05OTE0LTk1ZTQ4ZGZjOWRmMiIsImF1dGhfdGltZSI6MTUxMzk2NzA5Nywia2lkIjoicnNhMSIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4NS9vcGVuaWQtY29ubmVjdC1zZXJ2ZXItd2ViYXBwLyIsImV4cCI6MTUxMzk3MTQyMSwiaWF0IjoxNTEzOTcwODIxLCJqdGkiOiIxNzUyYjI4Mi0wYzljLTQwNGEtYmExNi1iNTE3ZjNhMjYyZjgifQ.sWZWFVAJ0ZXAjY1PiPTxVlC_CZ6ICmSbhpc0oG6dBnQ'
#
#
