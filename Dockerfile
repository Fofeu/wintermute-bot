FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/FofeuLabs/wintermute-bot.git

WORKDIR /usr/src/app/wintermute-bot

ENTRYPOINT ["python", "wintermute" ]
