FROM python:3.9

ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade -y

COPY --chown=${USER} requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

COPY --chown=${USER} ./custom_logger.py custom_logger.py
COPY --chown=${USER} ./main.py main.py
COPY --chown=${USER} ./Makefile Makefile

USER ${USER}

ENTRYPOINT ["python", "main.py"]