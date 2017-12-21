#!/usr/bin/env bash

curl 'http://localhost:8085/openid-connect-server-webapp/register' \
    -H 'Content-Type: application/json' \
    -H 'Origin: http://localhost:8085' \
    -X POST \
    -H "Authorization: Bearer eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJhZG1pbiIsImF6cCI6IjdjMmMwNzcxLTEzMWUtNGViYy05OTE0LTk1ZTQ4ZGZjOWRmMiIsImlzcyI6Imh0dHA6XC9cL2xvY2FsaG9zdDo4MDg1XC9vcGVuaWQtY29ubmVjdC1zZXJ2ZXItd2ViYXBwXC8iLCJleHAiOjE1MTM1NTIwNzIsImlhdCI6MTUxMzU0ODQ3MiwianRpIjoiYjZjYzMwYzYtYTY3Ny00MGI1LTg3YTQtZTdiZGQ0OWZjZTczIn0.EIANHdeBJzI-9p_5Cg4hV9GmoYGvbocMuCdTQkt3d2iVBuZ7lskLQ0344Zk3nZjLbSW8lqJOc-eH_AiztWkumtW-2yeF4hGjMm4KeRogzaSOimk6MVSLvgXwvJDhedZnlIHekxbk5GdKGLP06o8fdzZJKC3oChGhgfBbSXP4L_IP1-21q3nn90JRztvY6nZVYt3FrDPptzyEqM5bOWK9r1-E9T1p5p4-wC3ZOwDNFq7dsW0Jr54BIIe5391FmRtNUh_IrCulhEhR6EdAMp_CWecTsr2qx0UGjrWwNzk62XHz-C70SJaN1Km-RRzOq_UKYwwC08-N6ikKO2XE24Dj0A" \
    --data-binary @register.json \
    -vk