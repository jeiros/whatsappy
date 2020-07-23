FROM continuumio/anaconda3

WORKDIR /app

COPY requirements.txt .
ADD whatsappy whatsappy/
COPY setup.py .

RUN pip install -r requirements.txt && pip install .
