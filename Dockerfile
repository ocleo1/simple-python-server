FROM python:3.12-alpine

ARG PORT

ENV PORT=${PORT}

WORKDIR /srv

COPY . .

EXPOSE ${PORT}

HEALTHCHECK --interval=3s --timeout=3s --retries=3 \
    CMD python pulse.py

CMD [ "python", "-u", "server.py" ]
