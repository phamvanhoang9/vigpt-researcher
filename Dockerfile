FROM python:3.11-slim-bullseye as install-browser

RUN apt-get update \
    && apt-get satisfy -y \
    "chromium, chromium-driver (>= 115.0)" \
    && chromium --version && chromedriver --version

RUN apt-get install -y firefox-esr wget \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz \
    && tar -xvzf geckodriver* \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

FROM install-browser as vigpt-researcher-install

ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt 
RUN pip install -r requirements.txt

FROM vigpt-researcher-install as vigpt-researcher 

RUN useradd -ms /bin/bash vigpt-researcher \
    && chown -R vigpt-researcher:vigpt-researcher /usr/src/app 

USER vigpt-researcher 

COPY --chown=vigpt-researcher:vigpt-researcher ./ ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]