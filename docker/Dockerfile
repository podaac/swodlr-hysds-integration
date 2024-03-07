FROM python:3.10-alpine
ARG WHL_FILE

COPY ${WHL_FILE} .
RUN pip3 install *.whl
RUN rm *.whl
