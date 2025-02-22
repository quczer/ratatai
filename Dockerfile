FROM ubuntu:22.04 AS ratatai

LABEL org.opencontainers.image.source=https://github.com/quczer/ratatai

ENV USER=docker-user
ENV HOME=/home/${USER}
ENV UID=1000

ARG DEBIAN_FRONTEND=noninteractive
ARG REPO_PATH=/mnt/ratatai
ARG USER_GID=1000
ARG PIP_CACHE=${HOME}/.cache/pip

WORKDIR ${REPO_PATH}

RUN groupadd ${USER} --gid ${USER_GID} && useradd -l -m ${USER} -u ${UID} -g ${USER_GID} -s /bin/bash

RUN apt-get update && apt-get install --no-install-recommends -y lsb-release sudo tzdata bash-completion

# Utility
RUN sudo apt-get update && sudo apt-get install -y vim git git-lfs tcpdump tmux mc htop jq ffmpeg iputils-ping zip python3-pip

# Create non root user for pip
RUN echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER}
RUN chmod 0440 /etc/sudoers.d/${USER}

RUN mkdir -p ${HOME} && chown -R ${USER}:${USER} ${HOME}

USER ${USER}

RUN sudo ln -sf /usr/bin/python3 /usr/bin/python
RUN pip3 install --upgrade pip

RUN sudo apt-get install locales \
    && sudo locale-gen en_US en_US.UTF-8 \
    && sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
    && export LANG=en_US.UTF-8 && echo 'export LANG=en_US.UTF-8' >> ~/.bashrc

RUN sudo adduser ${USER} audio && sudo adduser ${USER} video

WORKDIR ${HOME}/pydeps
COPY --chown=${USER}:${USER} /backend backend
RUN --mount=type=cache,target=${PIP_CACHE},uid=${UID} pip install -e backend/

RUN pip uninstall -y ratatai

RUN echo "PS1='\[\033[1;38;5;214m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[0m\]\$ '" >> ~/.bashrc
RUN echo "export BETTER_EXCEPTIONS=1" >> ~/.bashrc

RUN echo "#!/bin/bash" > entrypoint.sh \
    && echo "set -e" >> entrypoint.sh \
    && echo "pip install -e backend/" >> entrypoint.sh \
    && echo 'exec "$@"' >> entrypoint.sh \
    && chmod +x entrypoint.sh \
    && sudo mv entrypoint.sh /entrypoint.sh

WORKDIR ${REPO_PATH}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
