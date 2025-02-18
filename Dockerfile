FROM python:3.8-slim

WORKDIR /test1

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libsqlite3-dev \
    freetds-bin \
    freetds-dev \
    tdsodbc && \
    rm -rf /var/lib/apt/lists/*



COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ['streamlit', 'run', 'test1.py']