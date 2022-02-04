

# Creating a python base with shared environment variables
FROM detectron2-docker_detectron2-cuda-11 as cuda-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# OpenCV dependencies
RUN apt update
RUN apt install ffmpeg libsm6 libxext6 -y
RUN apt install python3-pip git -y

# builder-base is used to build dependencies
FROM cuda-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Install gcloud.
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update
RUN apt-get install -y google-cloud-sdk

# Install cloudml-hypertune for hyperparameter tuning
RUN pip install --upgrade google-cloud-storage
RUN pip install --upgrade cloudml-hypertune gcloud

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev  # respects 

# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM builder-base as production
WORKDIR /app

ENV PORT 8000
ENV FASTAPI_ENV production
ENV DEFAULT_PATH /src

EXPOSE $PORT
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app
