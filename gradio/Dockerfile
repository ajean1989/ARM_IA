FROM python:3.11

WORKDIR /gradio

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 7860

COPY ./app .

RUN chmod +x /usr/local/bin/python
RUN chmod +x app.py

CMD ["sleep", "infinity"]
# CMD ["python", "app.py"]