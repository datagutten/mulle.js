FROM python:3 as builder_py
ARG GAME_LANG=sv
ARG OPTIPNG_LEVEL=7

WORKDIR /build
# Copy build scripts
COPY ./build_scripts ./build_scripts
COPY ./requirements.txt .
COPY ./assets.py .
COPY ./audiosprite ./audiosprite

# Copy game data
COPY ./iso/mullebil_${GAME_LANG}.iso ./iso/mullebil_${GAME_LANG}.iso
COPY ./iso/plugin.exe ./iso/plugin.exe

# Install dependencies
RUN apt-get update
RUN apt-get -y install ffmpeg optipng
RUN pip install -r requirements.txt

# Unpack iso
RUN python build_scripts/build.py ${GAME_LANG} download

# Create output folders
RUN mkdir -p dist/info/img

# Build scores and assets
RUN python build_scripts/build.py ${GAME_LANG} scores
RUN python assets.py ${OPTIPNG_LEVEL} assets_${GAME_LANG}

# Convert and copy UI images
RUN python build_scripts/build.py ui-images

# Build topograhy images
RUN python build_scripts/topography.py ./cst_out_new/CDDATA.CXT/Standalone ./topography


FROM node:18-bookworm as builder_js
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
RUN npm install -g sass
RUN sass ./src/style.scss ./dist/style.css

FROM httpd:bookworm as web_run
EXPOSE 80
ARG GAME_LANG=sv
WORKDIR /usr/local/apache2/htdocs

# Copy built assets
COPY --from=builder_py /build/assets_${GAME_LANG} ./assets
COPY --from=builder_js /build/dist .
COPY --from=builder_py /build/dist .

# Copy topograpchy sprite sheet
RUN mkdir ./assets/topography
COPY --from=builder_js /build/topography/topography.json ./assets/topography
COPY --from=builder_js /build/topography/topography.png ./assets/topography

# Copy static files from source
COPY ./src/index_cdn.html ./index.html
COPY ./data ./data
COPY ./info ./info
COPY ./progress ./progress

RUN echo ${GAME_LANG}