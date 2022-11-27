#!/bin/bash

CERT_FOLDER="./dev/certs"
CSR_FOLDER="./dev/certs/csrs"

openssl x509 -req \
    -days 360 \
    -in "${CSR_FOLDER}/$1.csr" \
    -CA "${CERT_FOLDER}/root_ca.crt" \
    -CAkey "${CERT_FOLDER}/root_ca.key" \
    -CAcreateserial \
    -out "${CERT_FOLDER}/$1.crt"

cp "${CSR_FOLDER}/$1.key" "${CERT_FOLDER}/$1.key"
