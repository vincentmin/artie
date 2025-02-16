FROM ghcr.io/astral-sh/uv:0.5.31-python3.12-bookworm-slim AS builder

ENV HOST=0.0.0.0
ENV LISTEN_PORT=8000
EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen && uv cache clean

# The runtime image, used to just run the code provided its virtual environment
FROM ghcr.io/astral-sh/uv:0.5.31-python3.12-bookworm-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /usr/bin/curl /usr/bin/curl
COPY --from=builder /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY main.py chainlit.md chainlit_nl-BE.md chainlit_nl-NL.md config_base.py config_moma.py config_tate.py config_rijks.py utils.py ./
COPY ./.chainlit ./.chainlit
COPY ./public ./public


HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=1m --start-interval=1s CMD curl -I http://0.0.0.0:8000 || exit 1

CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0"]
