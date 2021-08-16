# Docker container setup instructins go here.
FROM python:3.9

# set the working directory in the container
WORKDIR /app

# copy the content of the local directory to the working directory
COPY . .

# Install and upgrade pip
RUN pip install --upgrade pip

# copy the dependencies file to the working directory
COPY ./requirements.txt /app/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# Run Python script
RUN python src/importcsv2sql.py

# command to run on container start
CMD ["python","app.py"]

