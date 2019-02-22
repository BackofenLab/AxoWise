# Dockerfile for the web application

FROM continuumio/miniconda3

LABEL Name=pgdb-web Version=0.1
EXPOSE 5000

WORKDIR /pgdb-web

# Add all the files from the repository to the container
ADD . /pgdb-web

# Create the conda environment
RUN conda env create -f environment.yml

# Run the server
CMD /bin/bash -c "source activate pgdb && python server.py"
