FROM ubuntu:latest
LABEL authors="lucasoskorep"

ENTRYPOINT ["top", "-b"]