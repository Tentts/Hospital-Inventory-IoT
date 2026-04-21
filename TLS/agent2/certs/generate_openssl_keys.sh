openssl genrsa -out agent2-key.pem 2048
openssl req -new -sha256 -key agent2-key.pem -out agent2-csr.pem
openssl x509 -req -in agent2-csr.pem -signkey agent2-key.pem -out agent2-cert.pem