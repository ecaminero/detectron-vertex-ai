# Creating a python base with shared environment variables
FROM nvidia/cuda:11.3.1-devel-ubuntu20.04 as cuda-base

# cuda-env
ENV DEBIAN_FRONTEND noninteractive

# set PYTORCH_NO_CUDA_MEMORY_CACHING=1 in your environment to disable caching.
ENV PYTORCH_NO_CUDA_MEMORY_CACHING 0

# This will by default build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"

# set FORCE_CUDA because during `docker build` cuda is not accessible
ENV FORCE_CUDA 1
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Update
RUN apt-get update && apt-get install -y

# Install python pip 
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates wget python3-dev git sudo ninja-build python3-pip

RUN ln -sv /usr/bin/python3 /usr/bin/python


# Python Pyenv 
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
RUN pip install poethepoet

# Install cloudml-hypertune for hyperparameter tuning
RUN pip install --upgrade google-cloud-storage
RUN pip install --upgrade cloudml-hypertune gcloud

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
# Install Pip Package with poe
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
COPY ./model ./model

# poetry packages
RUN poetry install --no-dev  # respects 
RUN poe torch 
RUN poe detectron2

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

CMD exec uvicorn src.main:app --host 0.0.0.0 --port $PORT
