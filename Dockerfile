# app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/WazaCraft/templatizer.git .

RUN pip3 install -r requirements.txt

EXPOSE 80

ENV STREAMLIT_SERVER_PORT=80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "template-tool.py", "--server.port=80", "--server.address=0.0.0.0"]
