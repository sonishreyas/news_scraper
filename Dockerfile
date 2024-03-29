# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.6-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /app
# USER appuser
# RUN chown appuser:appuser -R /app/

RUN export PYTHONPATH="/app"
# RUN export GOOGLE_APPLICATION_CREDENTIALS="/app/src/configs/key.json"
# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/src/configs/key.json"
ENV PYTHONPATH="/app"
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT [ "python3","/app/src/main.py" ]
CMD ["/app/src/main.py"]
