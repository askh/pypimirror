FROM python
EXPOSE 3141
RUN apt update && apt upgrade -y
RUN useradd -d /home/devpisrv -m -s /bin/bash -U devpisrv
RUN mkdir -p -m 750 /var/local/devpisrv && mkdir -m 750 /var/local/devpisrv/server && mkdir -m 750 /var/local/devpisrv/config && chown -R devpisrv:devpisrv /var/local/devpisrv
COPY --chown=devpisrv:devpisrv .env* /var/local/devpisrv/config/
COPY requirements.txt /tmp/
USER devpisrv:devpisrv
RUN pip3 install -U pip
ENV PATH="/home/devpisrv/.local/bin:${PATH}"
RUN pip install -U -r /tmp/requirements.txt
COPY src/devpisrv.py /usr/local/bin/
ENTRYPOINT ["devpisrv.py", "--overwrite-config"]

