FROM python:3.11.6-slim-bookworm

COPY . /repo
RUN pip install --no-cache-dir /repo \
    && rm -fr /repo

RUN adduser --disabled-password --uid 10000 auralmatics \
    && mkdir /app \
    && chown auralmatics:auralmatics /app

USER auralmatics
WORKDIR /app

COPY --chown=auralmatics .streamlit /app/.streamlit
COPY --chown=auralmatics data /app/data

ENV STREAMLIT_SERVER_RUN_ON_SAVE='false' \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE='none'
EXPOSE 8501
ENTRYPOINT ["auralmatics"]
