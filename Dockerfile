FROM python:3.9-slim as base

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY . .

# Production 
FROM base as production

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

# Development
FROM base as development

RUN poetry install

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]  

FROM base as test

RUN poetry install

CMD ["poetry", "run", "pytest"]  