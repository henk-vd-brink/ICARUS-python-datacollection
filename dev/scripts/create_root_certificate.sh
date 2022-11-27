#!/bin/bash

CERT_FOLDER="./dev/certs"

openssl req -x509 \
            -sha256 -days 356 \
            -nodes \
            -newkey rsa:2048 \
            -subj "/CN=icarus.com/C=NL/ST=Zuid-Holland/L=Delft" \
            -keyout ${CERT_FOLDER}/root_ca.key -out ${CERT_FOLDER}/root_ca.crt
