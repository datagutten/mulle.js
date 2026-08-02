# Override this step with additional_contexts in docker-compose.yml if ISO is outside project directory
FROM scratch AS iso
ARG GAME_LANG=sv
COPY ./iso/mullebil_${GAME_LANG}.iso mullebil_${GAME_LANG}.iso
COPY ./iso/plugin.exe plugin.exe

FROM python:3.14 AS builder_py
# Install dependencies
RUN apt-get update && apt-get -y install ffmpeg optipng
RUN pip install --upgrade pip poetry poetry-plugin-export
COPY pyproject.toml .
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

ARG GAME_LANG=sv
ARG OPTIPNG_LEVEL=7

WORKDIR /build
ENV PYTHONPATH=/build
# Copy build scripts
COPY ./build_scripts ./build_scripts
COPY build_scripts/assets/audiosprite ./audiosprite

# Copy game data
COPY --from=iso mullebil_${GAME_LANG}.iso ./iso/mullebil_${GAME_LANG}.iso
COPY --from=iso plugin.exe ./iso/plugin.exe

# Unpack iso
RUN python build_scripts/build.py ${GAME_LANG} download

# Create output folders
RUN mkdir -p dist/info/img

# Build scores and assets
RUN python build_scripts/build.py ${GAME_LANG} scores
RUN python build_scripts/build.py ${GAME_LANG} assets

# Convert and copy UI images
RUN python build_scripts/build.py ${GAME_LANG} ui-images

# Build topograhy images
RUN python build_scripts/topography.py ./cst_out_new/CDDATA.CXT/Standalone ./topography


FROM node:24 AS builder_js
ARG SERVER_ADDRESS
ENV SERVER_ADDRESS=${SERVER_ADDRESS}

WORKDIR /build

# Install dependencies
COPY ./package.json .
COPY ./package-lock.json .
RUN npm install

# Build topography sprite sheet
COPY --from=builder_py /build/topography ./topography
COPY ./build_scripts/topography.js .
RUN node ./topography.js ./topography

 # Copy source
COPY ./src ./src
COPY ./webpack.common.js .
COPY ./webpack.prod.js .

# Build webpack
RUN npx webpack-cli -c webpack.prod.js

# Build sass
RUN npx sass src/style.scss dist/style.css

FROM httpd:bookworm AS web_run
EXPOSE 80
ARG GAME_LANG=sv
WORKDIR /usr/local/apache2/htdocs

# Copy static files from source
COPY ./src/index_cdn.html ./index.html
COPY ./data ./data
COPY ./info ./info
COPY ./progress ./progress

# Copy topograpchy sprite sheet
RUN mkdir -p assets/topography
COPY --from=builder_js /build/topography/topography.json ./assets/topography
COPY --from=builder_js /build/topography/topography.png ./assets/topography

# Copy built assets
COPY --from=builder_js /build/dist .
COPY --from=builder_py /build/assets_${GAME_LANG} ./assets
COPY --from=builder_py /build/dist .

RUN echo ${GAME_LANG}