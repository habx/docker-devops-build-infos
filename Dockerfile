FROM python:3-alpine
WORKDIR /work
COPY . /build
CMD /build/run.sh
