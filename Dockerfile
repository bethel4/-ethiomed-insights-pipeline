FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -i https://pypi.org/simple -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"] 