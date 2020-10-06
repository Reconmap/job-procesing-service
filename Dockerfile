FROM python:3

WORKDIR /opt/reconmap-job-processing-svc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ./

EXPOSE 8765

CMD ["python3", "src/main.py"]

