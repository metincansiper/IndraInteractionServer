FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get update --fix-missing && \
    apt-get install -y git && \
    apt-get install wget


RUN git clone https://github.com/sorgerlab/bioagents.git

RUN wget -nv "http://www.csb.pitt.edu/Faculty/Faeder/wp-content/uploads/2017/04/BioNetGen-2.2.6-stable_Linux.tar.gz" \
        -O BioNetGen.tar.gz && \
        tar xzf BioNetGen.tar.gz

ENV PYTHONPATH "${PYTHONPATH}:/bioagents:/BioNetGen-2.2.6-stable:/usr/lib/python3.7/site-packages"

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
ADD ./indra-interaction-server /app/indra-interaction-server

ENV LANG C.UTF-8
RUN apt-get install -y python3-pygraphviz
RUN pip3 install -r requirements.txt

RUN chmod +x /app/indra-interaction-server/server.py
EXPOSE 8000
ENTRYPOINT [ "python3", "/app/indra-interaction-server/server.py" ]
