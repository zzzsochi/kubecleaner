FROM python:3.7-alpine AS build

ADD setup.py /srv/src/setup.py
ADD kubecleaner /srv/src/kubecleaner
RUN \
 apk add --update build-base openssl-dev libffi-dev && \
 pip install -U pip wheel && \
 pip wheel --wheel-dir=/srv/wheels /srv/src/

FROM python:3.7-alpine

COPY --from=build /srv/wheels /srv/wheels
RUN pip install /srv/wheels/* && rm -rf /srv/wheels

ENTRYPOINT ["/usr/local/bin/python3", "-m", "kubecleaner"]
CMD ["--help"]
