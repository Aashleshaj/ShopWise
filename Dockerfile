FROM python:3.13-slim
ENV MICRO_SERVICE=/home/app/webapp
# passing argument from build stage to environment variable
ARG SDLC_ARG
ENV SDLC_ENV=${SDLC_ARG}

# set work directory
RUN mkdir -p $MICRO_SERVICE
# where your code lives

WORKDIR $MICRO_SERVICE
# set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN pip install --upgrade pip

#COPY src/ $MICRO_SERVICE
COPY ./scripts/app.py   $MICRO_SERVICE
COPY ./requirements.txt   $MICRO_SERVICE
RUN pip install -r requirements.txt
EXPOSE 8501
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0