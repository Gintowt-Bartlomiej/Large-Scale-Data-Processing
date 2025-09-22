FROM alpine:latest

ARG MESSAGE="test message"

ENV MESSAGE_ENV=$MESSAGE

RUN apk add --no-cache figlet

ADD ascii.txt /ascii.txt

ENTRYPOINT ["sh", "-c"]

CMD ["figlet \"$MESSAGE_ENV\" && cat /ascii.txt"]
