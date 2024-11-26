FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
WORKDIR /app
#COPY pyproject.toml README.md .
#COPY xiaomusic/ ./xiaomusic/
#COPY plugins/ ./plugins/
#COPY xiaomusic.py .
RUN rm-rf .* * && git clone https://github.com/dissipator/xiaomusic.git .  && git checkout dev
COPY pyproject.toml .
RUN pdm install --prod --no-editable

