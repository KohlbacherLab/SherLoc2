# Applied Bioinformatics Group
# SherLoc2 Docker Image
#
# Philipp Thiel

FROM ubuntu:14.04

# Update package repository
RUN apt-get update
#RUN apt-get -y upgrade


# ----------------------------------------------------------
# Install some useful and required stuff
# ----------------------------------------------------------
RUN apt-get install -y dirmngr software-properties-common vim wget


# ----------------------------------------------------------
# Install LibSVM and BLAST
# ----------------------------------------------------------
RUN apt-get install -y libsvm-tools ncbi-blast+


# ----------------------------------------------------------
# Install InterProScan dependencies
# ----------------------------------------------------------
RUN apt-get install -y libgnutls28

RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update

RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN apt-get install -y -q --no-install-recommends oracle-java8-installer
RUN apt-get install -y -q oracle-java8-set-default

ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/bin


# ----------------------------------------------------------
# Setup MultiLoc2 Webservice
# ----------------------------------------------------------
RUN apt-get -y install python-biopython apache2
RUN a2enmod cgid
ADD webservice/apache2.conf         /etc/apache2/apache2.conf
ADD webservice/serve-cgi-bin.conf   /etc/apache2/conf-available/serve-cgi-bin.conf

COPY webservice/webloc.cgi   /var/www/html/cgi-bin/
COPY webservice/epiloc_interface.py   /var/www/html/cgi-bin/
COPY webservice/dialoc_interface.py   /var/www/html/cgi-bin/
COPY webservice/downloads/   /var/www/html/cgi-bin/downloads/
COPY webservice/images/      /var/www/html/cgi-bin/images/

RUN mkdir /webservice
ADD webservice/job_cleanup.sh          /webservice/job_cleanup.sh
ADD webservice/sl2setup.py             /webservice/sl2setup.py
ADD webservice/sherloc2_entrypoint.sh  /webservice/sherloc2_entrypoint.sh

RUN mkdir /sl2jobs
RUN chmod 777 /sl2jobs

# ----------------------------------------------------------
# Install MultiLoc2
# ----------------------------------------------------------
COPY SherLoc2 /SherLoc2
WORKDIR /SherLoc2
RUN python configureSL2Online.py

WORKDIR /
RUN  chown -R www-data:www-data /SherLoc2
RUN  chmod -R 775 /SherLoc2


EXPOSE 80

CMD ["sh", "/webservice/sherloc2_entrypoint.sh"]
