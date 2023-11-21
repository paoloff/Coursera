FROM python:3.11.5

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./spacex_dash_app.py /app/spacex_dash_app.py

COPY ./3.png /app/3.png

COPY ./spacex_launch_dash.csv /app/spacex_launch_dash.csv

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 3000

CMD ["python","spacex_dash_app.py"]
