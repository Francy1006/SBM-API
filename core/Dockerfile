FROM python:3.9

# apt-get installs
RUN apt-get update && \
    apt-get --no-install-recommends install -y build-essential nano \
    libpq-dev pkg-config \
    && apt-get clean

# upgrade pip
RUN pip install --upgrade pip

RUN pip

WORKDIR /usr/src/app

# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONNONBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]