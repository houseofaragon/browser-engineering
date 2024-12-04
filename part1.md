For HTTP - Netcat
`echo -e "GET /path HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n" | nc example.com 80`

For HTTPS (Port 443) - OpenSSL
Netcat does not support encrypted communication. Use openssl instead:
`echo -e "GET / HTTP/1.1\r\nHost: karenaragon.com\r\nConnection: close\r\n\r\n" | openssl s_client -connect karenaragon.com:443`