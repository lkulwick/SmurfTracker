FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY shim/requirements.txt ./shim/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./shim/requirements.txt

COPY shim ./shim

EXPOSE 8191

CMD ["uvicorn", "shim.app:app", "--host", "0.0.0.0", "--port", "8191"]
