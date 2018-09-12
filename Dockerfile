FROM python:3-alpine
COPY . /build
RUN /build/run.sh
