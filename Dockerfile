
FROM python:3.11.5

WORKDIR /convutell

COPY requirements.txt .
COPY convutell .

RUN python -m venv /opt/venv


RUN /opt/venv/bin/python -m pip install --upgrade pip

# Instalar o Supervisor
RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Instalar as dependências desencontradas  -- isso será alterado
RUN /opt/venv/bin/python -m pip install python-dotenv
RUN apt-get update && apt-get install -y libsmbclient-dev
RUN apt-get update && apt-get install -y libgirepository1.0-dev
RUN /opt/venv/bin/python -m pip install --no-cache-dir -r requirements.txt
RUN /opt/venv/bin/python -m pip install uvicorn



EXPOSE 8000 8501

#CMD ["/opt/venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

CMD supervisord -c /etc/supervisor/conf.d/supervisord.conf