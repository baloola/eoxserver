FROM geodata/gdal

ADD requirements.txt install.sh /
WORKDIR /
RUN /install.sh
ADD dbms /opt/dbms
WORKDIR /opt/dbms

EXPOSE 8000

CMD ["gunicorn", "--chdir", "dbms", "--bind", ":8000", "dbms.wsgi:application", "--workers", "10",  "--worker-class", "eventlet", "--timeout", "600"]
