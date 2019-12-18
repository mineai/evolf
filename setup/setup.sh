# This is the setup file to install the thing in a linux environment.

root_directory=${PWD##*/}

if [ "$root_directory" == "evolf" ]; then
  echo "Conitinuing"
else
  echo "Wrong Directory, Make sure you are in the root of evolf"
  exit 1
fi

# Add Current Path to ENV var
export PATH=$PATH:$PWD

# Add AWS Endpoints for Studio
## Note: To use Minio, these must be changed
export DOMAIN_DATA_ENDPOINT=http://s3.us-west-2.amazonaws.com
export STUDIO_DATABASE_ENDPOINT=http://s3.us-east-1.amazonaws.com/
export STUDIO_STORAGE_ENDPOINT=http://s3.us-east-1.amazonaws.com/

# All Functions go Here
function install_linux {
  echo "You are on a Linux System"
  apt-get update
  apt-get install -y vim
  apt-get install -y python3
  apt-get install -y python3-pip
}

function install_mac {
  echo "You are on a MAC"
}

# Run Commands according to OS
if [[ "$OSTYPE" == "linux-gnu" ]]; then
  install_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
  install_mac
else
  echo "Unknown OS"
fi

pip3 install virtualenv
virtualenv -p python3 .
source bin/activate

pip install -r setup/requirements.txt

