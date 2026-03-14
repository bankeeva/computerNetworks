FROM python:3.11

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    libnspr4 \
    libnss3 \
    libatk1.0-0 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libcairo2 \
    fonts-liberation \
    libglib2.0-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary pandas playwright

RUN playwright install chromium

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]