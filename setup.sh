# This is the setup file to install the thing in a linux environment.
apt-get install python
apt-get install python3
apt-get install python-pip
apt-get install python3-pip

pip3 install -r requirements.txt

echo ""
echo "To start string evolution server, Run: "
echo "python3 evolutionary_algorithms/domains/strevolve/flask_app/server.py"
