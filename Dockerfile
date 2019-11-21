# Python 3
FROM python:3.7.3-stretch

# File Author / Maintainer
MAINTAINER Eddie Belter <ebelter@wustl.edu>

# Deps
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  default-jre \
  less \
  libnss-sss \
  gcc \
  man \
  perl \
  sqlite3 \
  xz-utils \
  vim && \
  apt-get clean

# Install CANU
WORKDIR /apps/
RUN curl https://github.com/marbl/canu/releases/download/v1.8/canu-1.8.Linux-amd64.tar.xz -L -o canu-v1.8.tgz && \
  tar xJfvv canu-v1.8.tgz && \
  rm -rf canu-v1.8.tgz

RUN curl https://downloads.sourceforge.net/project/gnuplot/gnuplot/5.2.6/gnuplot-5.2.6.tar.gz -L -o gnuplot-5.2.6.tar.gz && \
  tar zxvvf gnuplot-5.2.6.tar.gz
WORKDIR /apps/gnuplot-5.2.6/
RUN ./configure && \
  make && \
  make check && \
  make install
WORKDIR /apps/
RUN rm -rf gnuplot-5.2.6*

# Install samtools
WORKDIR /tmp/samtools/
COPY samtools/samtools-1.9/ ./
RUN ./configure --prefix=/usr/local && \
  make && \
  make install
WORKDIR /tmp/
RUN rm -rf samtools

# Install LAH
WORKDIR /tmp/build/
COPY ./ ./
RUN pip install .
COPY etc/profile.d/lah.sh /etc/profile.d/
WORKDIR /
RUN rm -rf /tmp/build/

# Environment
ENV TZ=America/Chicago \
  MGI_NO_GAPP=1 \
  LANG=C \
  LSF_SERVERDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/etc \
  LSF_LIBDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/lib \
  LSF_BINDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/bin \
  LSF_ENVDIR=/opt/lsf9/conf \
  PATH="/apps/canu-1.8/Linux-amd64/bin:/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/bin:${PATH}"

WORKDIR /
CMD [/bin/bash, --login]
