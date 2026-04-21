openssl genrsa -out key.key 2048
openssl req -new -sha256 -key key.key -out csr.crt
openssl x509 -req -in csr.crt -signkey key.key -out cert.crt