FROM python:3.11

WORKDIR /gradio

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 7860

COPY ./app/ .

CMD ["python ./app.py"]