apt-get update
apt-get install -y python python-pip libpq-dev

pip install -r requirements.txt

# spiceypy is a bit finicky...
pip install -U six numpy urllib3 setuptools
pip install spiceypy

# Clean up.
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/partial/* /tmp/* /var/tmp/*
