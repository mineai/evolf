# This is the setup file to install the thing in a linux environment.
apt-get update
apt-get install -y vim
apt-get install -y python
apt-get install -y python3
apt-get install -y python-pip
apt-get install -y python3-pip

pip3 install -r requirements.txt

echo ""
echo "To start string evolution server, Run: "
echo "python3 evolutionary_algorithms/domains/strevolve/flask_app/server.py"


