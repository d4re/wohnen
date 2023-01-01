FROM python:3.10-slim

WORKDIR /workspace
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . /workspace/

ENTRYPOINT [ "python" ]
CMD ["/workspace/main.py"]