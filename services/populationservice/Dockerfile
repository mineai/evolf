# Specify Base Image
FROM ubuntu:18.04

# Make A new Directory and set it as default
WORKDIR /mineai/evolf/

# Copy Important Directories
COPY . .

## Run several Commands
RUN ["chmod", "+x", "setup.sh"]
RUN ./setup.sh

# Set Startup Command
CMD ["python3", "-m", "population_server"]


