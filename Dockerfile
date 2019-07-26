FROM ubuntu

RUN apt-get update && apt-get install --no-install-recommends -y  python3 python3-pip python3-setuptools && pip3 install cloudgenix && pip3 install Flask && apt-get remove -y python3 python3-pip && apt-get autoremove -y && apt-get install -y python3-idna && rm -rf /var/lib/apt/lists/*

ADD . /cgxBlocks
WORKDIR /cgxBlocks
ENV FLASK_APP=cgxBlocks.py
ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000

#ENTRYPOINT [ "flask","run" ]
ENTRYPOINT flask run --host 0.0.0.0
