#!/bin/bash

CERT_FOLDER="./dev/certs/csrs"

openssl req \
    -new -newkey rsa:2048 -nodes \
    -subj "/C=NL/ST=Zuid-Holland/L=Delft/CN=$1" \
    -keyout "${CERT_FOLDER}/$1.key" \
    -out "${CERT_FOLDER}/$1.csr"
