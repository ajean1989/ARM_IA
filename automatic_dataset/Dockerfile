FROM python:3.11

WORKDIR /automatic_dataset

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && apt install nano

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt
CMD ["sleep", "infinity"]
#CMD ["python", "-m",  "pytest",  "-sv"] 



