# Specify Base Image
FROM python:alpine

# Make A new Directory and set it as default
WORKDIR /mineai/evolf/

# Run several Commands
RUN setup/setup.sh

# Copy files from this folder
COPY . .

# Set Startup Command
CMD ["python3", "-m", "population_server"]


