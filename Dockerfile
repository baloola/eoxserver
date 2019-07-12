FROM geodata/gdal

RUN mkdir /opt/eoxserver/

ADD eoxserver /opt/eoxserver/eoxserver
ADD tools /opt/eoxserver/tools
ADD setup.cfg setup.py MANIFEST.in README.rst requirements.txt /opt/eoxserver/

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list && \
  apt-get update && \
  apt-get install -y \
    python \
    python-pip \
    libpq-dev \
    libgdal1h libgeos-c1 libmapserver1\
    python-mapscript && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/partial/* /tmp/* /var/tmp/*

# install EOxServer and its dependencies
WORKDIR /opt/eoxserver

RUN pip install -r requirements.txt && \
  pip install .

# Create an EOxServer instance
RUN mkdir /opt/instance && \
  eoxserver-instance.py instance /opt/instance

EXPOSE 8000

CMD ["gunicorn", "--chdir", "/opt/instance", "--bind", ":8000", "instance.wsgi:application", "--workers", "10",  "--worker-class", "eventlet", "--timeout", "600"]
