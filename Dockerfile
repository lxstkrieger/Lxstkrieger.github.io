FROM python:3.11

WORKDIR /bot

# Copy only necessary files first to leverage Docker cache
COPY requirements.txt ./
COPY .env ./
COPY main.py ./
COPY cogs/ ./cogs/
COPY databases/ ./databases/

# Combine multiple COPY commands into one
COPY cogs/baka.py cogs/ban.py cogs/bans.py cogs/clear.py cogs/help.py \
     cogs/hug.py cogs/kick.py cogs/kiss.py cogs/cry.py cogs/dance.py \
     cogs/Levelsystem.py cogs/memes.py cogs/punch.py cogs/serverinfo.py \
     cogs/TempVoice.py cogs/Ticketsystem.py cogs/TiktakToo.py cogs/timeout.py \
     cogs/unban.py cogs/userinfo.py cogs/Warnsystem.py cogs/Music.py /bot/cogs/

COPY databases/Levelsystem.db databases/Warnsystem.db /bot/databases/

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

CMD python main.py
