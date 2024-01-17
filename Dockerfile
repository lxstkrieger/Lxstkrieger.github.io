FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
COPY .env /bot/
COPY main.py /bot/
COPY /cogs/baka.py /bot/cogs/
COPY /cogs/ban.py /bot/cogs/
COPY /cogs/bans.py /bot/cogs
COPY /cogs/clear.py /bot/cogs
COPY /cogs/gameNews.py /bot/cogs
COPY /cogs/help.py /bot/cogs
COPY /cogs/hug.py /bot/cogs
COPY /cogs/kick.py /bot/cogs
COPY /cogs/kiss.py /bot/cogs
COPY /cogs/levelsystem.py /bot/cogs
COPY /cogs/memes.py /bot/cogs
COPY /cogs/punch.py /bot/cogs
COPY /cogs/serverinfo.py /bot/cogs
COPY /cogs/TempVoice.py /bot/cogs
COPY /cogs/ticketsystem.py /bot/cogs
COPY /cogs/TiktakToo.py /bot/cogs
COPY /cogs/timeout.py /bot/cogs
COPY /cogs/unban.py /bot/cogs
COPY /cogs/userinfo.py /bot/cogs
COPY /cogs/warnsystem.py /bot/cogs
COPY /databases/Levelsystem.db /bot/databases
COPY /databases/Warnsystem.db /bot/databases

RUN pip install -r requirements.txt
COPY . /bot
CMD python bot.py

