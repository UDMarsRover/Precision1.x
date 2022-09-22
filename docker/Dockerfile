

FROM ros:melodic AS presision1

ARG branch=Greg

RUN useradd udmrt
USER udmrt
COPY ./entrypoint.sh /home/udmrt/
USER root
RUN chmod +x /home/udmrt/entrypoint.sh && \
    chown -R udmrt /home/udmrt


USER udmrt
WORKDIR /home/udmrt
RUN cd /home/udmrt && \
    git clone https://github.com/UDMarsRover/precision1.git
    
WORKDIR /home/udmrt/precision1
RUN git checkout ${branch} && \
    git pull    

EXPOSE 11311/tcp

ENTRYPOINT [ "/home/udmrt/entrypoint.sh" ]
CMD ["bash"]