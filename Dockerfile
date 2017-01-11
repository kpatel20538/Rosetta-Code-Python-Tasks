FROM python:3-alpine

RUN apk update
RUN apk upgrade

RUN apk add curl gcc g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install numpy

RUN apk add libjpeg-turbo lcms2 openjpeg tiff libwebp
RUN apk add zlib zlib-dev jpeg jpeg-dev libpng libpng-dev
RUN pip install Pillow

RUN mkdir -p /usr/rosetta
RUN mkdir -p /usr/rosetta/tasks
RUN mkdir -p /usr/rosetta/tests
RUN mkdir -p /usr/rosetta/logs
RUN mkdir -p /usr/rosetta/out
RUN touch /usr/rosetta/tasks/__init__.py
RUN touch /usr/rosetta/tests/__init__.py

COPY finished /usr/rosetta/tasks
COPY incomplete /usr/rosetta/tasks
RUN mv /usr/rosetta/tasks/*_test.py /usr/rosetta/tests/

WORKDIR /usr/rosetta
ENTRYPOINT ["python","-m"]
