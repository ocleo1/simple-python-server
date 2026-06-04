FROM python:3.12-alpine

ARG PORT

ENV PORT=${PORT}

WORKDIR /srv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE ${PORT}

HEALTHCHECK --interval=3s --timeout=3s --retries=3 \
    CMD python pulse.py

CMD [ "uv", "run", "python", "-u", "server.py" ]
