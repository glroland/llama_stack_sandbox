FROM registry.access.redhat.com/ubi9/python-311:latest

# By default, listen on port 8080
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /projects

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./src/ .

# Specify the command to run on container start
#CMD [ "python", "app.py" ]
CMD [ "python", "calc_mcp_server.py" ]
