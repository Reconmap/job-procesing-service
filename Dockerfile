FROM python:3

WORKDIR /opt/reconmap-job-processing-svc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN echo 127.0.0.1 localhost > /etc/hosts

COPY . ./

EXPOSE 8765

CMD ["python", "./main.py"]

