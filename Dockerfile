FROM ubuntu:14.04.1

# basic toolbelt
RUN apt-get update
RUN apt-get install -y build-essential git
RUN apt-get install -y python python-dev python-setuptools
RUN apt-get install -y nginx
RUN apt-get install -y wget
RUN easy_install pip
RUN pip install uwsgi

# install wkhtmltopdf
RUN wget http://downloads.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb -O /tmp/wkhtmltox-0.12.1_linux-trusty-amd64.deb
# seems to be no easy way to auto install the dependencies of wkhtmltopdf so we're manually 
# installing everything listed by "dpkg -I wkhtmltox-0.12.1_linux-trusty-amd64.deb"
RUN apt-get install -y fontconfig libfontconfig1 libfreetype6 libpng12-0 zlib1g libjpeg-turbo8\
 libssl1.0.0 libx11-6 libxext6 libxrender1 libstdc++6 libc6
RUN dpkg -i /tmp/wkhtmltox-0.12.1_linux-trusty-amd64.deb

# setup pdfapi inside docker
ADD pydf /src/pydf
ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
ADD pdfapi.py /src/pdfapi.py

# allow access from port 5000
EXPOSE 5000

# set environment variable to indicate we're inside docker
ENV DOCKER 1

CMD ["python", "/src/pdfapi.py"]
