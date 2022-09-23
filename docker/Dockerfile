

FROM ros:melodic AS presision1

RUN useradd udmrt
USER udmrt
COPY entrypoint.sh /home/udmrt/
COPY branch.txt /home/udmrt/
USER root
RUN chmod +x /home/udmrt/entrypoint.sh && \
    chown -R udmrt /home/udmrt


USER udmrt
WORKDIR /home/udmrt
RUN cd /home/udmrt && \
    git clone https://github.com/UDMarsRover/precision1.git
