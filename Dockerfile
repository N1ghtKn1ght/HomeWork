FROM python:3
EXPOSE 8000

RUN git clone https://github.com/N1ghtKn1ght/HomeWork.git
RUN pip install --no-cache-dir -r /HomeWork/requirements.txt

