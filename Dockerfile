FROM ubuntu:latest

RUN apt-get update && apt-get install -y -q \
    wget \
    tar \
    curl \
    tzdata \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install requests --break-system-packages

WORKDIR /app

COPY x-ui-linux-amd64.tar.gz /app/

RUN tar -xvzf x-ui-linux-amd64.tar.gz

COPY x-ui.py /app/x-ui/

WORKDIR /app/x-ui/

RUN chmod +x x-ui

ENV PATH="/app/x-ui:${PATH}"

CMD ["bash"]