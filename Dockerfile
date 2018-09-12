FROM python:3-alpine
WORKDIR /work
RUN apk update && apk add git
COPY . /build
CMD /build/run.sh
