FROM alpine:latest

LABEL source_repository="https://github.com/sapcc/vcsa-exporter"
RUN apk --update add python3 openssl ca-certificates bash python3-dev  git py3-pip && \
    apk --update add --virtual build-dependencies libffi-dev openssl-dev libxml2 libxml2-dev libxslt libxslt-dev build-base
RUN git config --global http.sslVerify false
#RUN git clone https://github.com/sapcc/vrops-exporter.git
RUN pip3 install --upgrade pip

ADD . vcsa-exporter/
RUN pip3 install --upgrade -r vcsa-exporter/requirements.txt

WORKDIR vcsa-exporter 
