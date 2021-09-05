#!/bin/bash

# Find out GNU/Linux version and distribution
if [ -f /etc/os-release ]; then
	. /etc/os-release
	OS=$NAME
	VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
	OS=$(lsb_release -si)
	VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
	. /etc/lsb-release
	OS=$DISTRIB_ID
	VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
	OS=Debian
	VER=$(cat /etc/debian_version)
else
	OS=$(uname -s)
	VER=$(uname -r)
fi

# Check GNU/Linux distribution, version and MySQL server has been installed or not
if [[ $OS == 'Ubuntu' ]]; then
	if (($(echo "$VER >= 18.04" | bc -l))); then
		# Check if MySQL server is installed or not
		if (dpkg -l | grep -Fq "mysql-server"); then
			read -rep "Warning: You already have MySQL server installed on your system. This script will modify your MySQL configuration. And this may cause data loss in your databases. Please follow the installation manually according to the Wikis. If you insist to follow setup procedures, please type YES. In the case of exit, press any other keys: " follow
			if [[ $follow != 'YES' ]]; then
				exit 0
			fi
		fi
	else
		echo "Unfortunately we're not support your operating system officially. But you can follow our instruction in the Wikis to install chatbot manually or use Docker to install this chatbot."
		exit 0
	fi
else
	echo "Unfortunately we're not support your operating system officially. But you can follow our instruction in the Wikis to install chatbot manually or use Docker to install this chatbot."
	exit 0
fi

# Set environment virables
echo "Set environment virables from .env file"

set -a
source production/.env
set +a

if [[ $OS == 'Ubuntu' && (($(echo "$VER >= 18.04" | bc -l))) ]]; then
	# Install chatbot dependencies
	echo "Install requirements"
	sudo apt-get update
	sudo apt-get install -y wget build-essential python3.8 python3.8-dev python3.8-venv python3-pip mysql-server libmysqlclient-dev

	sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
	sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld

	sudo apt install -f
	
	# Download and install libmysqlclient20 in the case of newer version of Ubuntu, which libmysqlclient20 is replaced by libmysqlclient21
	if (($(echo "$VER > 18.04" | bc -l))); then
		TEMP_DEB="$(mktemp)"
		wget -O "$TEMP_DEB" 'http://security.ubuntu.com/ubuntu/pool/main/m/mysql-5.7/libmysqlclient20_5.7.35-0ubuntu0.18.04.1_amd64.deb'
		sudo dpkg -i "$TEMP_DEB"
		rm -f "$TEMP_DEB"
  	fi

	# Configure MySQL server
	echo "Configure MySQL settings"

	# Change mysql user password plugin to mysql_native_password
	sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}'"

	# Make our changes take effect
	sudo mysql -u ${SQL_USER} -p${MYSQL_ROOT_PASSWORD} -e "FLUSH PRIVILEGES"

	# Create mysql database for datasets storing
	sudo mysql -u ${SQL_USER} -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE}"

	# Create mysql database to store logs
	sudo mysql -u ${SQL_USER} -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_EVENTS_DATABASE}"

	# Load datasets to the MySQL server
	echo "Load mysql dumps to the dataset"

	# Change charset of MySQL dump
	sed -i 's/utf8mb4_0900_ai_ci/utf8_general_ci/g' production/mysql-server/datasets.sql
	sed -i 's/utf8mb4/utf8/g' production/mysql-server/datasets.sql
	mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" datasets <production/mysql-server/datasets.sql
fi

# Create python virtual environment for rasa chatbot
echo "Create virtual environment for rasa"
python3.8 -m venv ~/.env/rasa_env
source ~/.env/rasa_env/bin/activate

# Install python requirements
pip install --upgrade pip
pip install -r production/rasa-server/requirements.txt -r production/action-server/requirements.txt

echo "Download spacy mode weights"
python -m spacy download en_core_web_md

echo "Make data directory in rasa"
mkdir -p production/rasa-server/autocorrect/data
(
	cd production/rasa-server
	python -c "import autocorrect; autocorrect.Speller('en_med')"
)

envsubst <production/rasa-server/rasa/endpoints.yml | tee production/rasa-server/rasa/endpoints.yml >/dev/null

echo "Download model weights"
mkdir -p production/rasa-server/rasa/models production/rasa-server/rasa/logs
wget -c https://www.dropbox.com/s/u1o8s2u96lpt8cv/v0.1.0.tar.gz -P production/rasa-server/rasa/models

# Configure action server
mkdir -p production/action-server/logs
cp production/.env production/action-server/.env

# UI server
echo "Create virtual environment for Streamlit UI"
python3.8 -m venv ~/.env/ui_env
source ~/.env/ui_env/bin/activate

# Install python requirements
pip install --upgrade pip
pip install -r production/streamlit-server/requirements.txt

# Configure UI server
cp production/.env production/streamlit-server/.env

echo -e "It's Done. Run the following commands to start chatbot\n
In the $(pwd)/production/action-server directory:
(source ~/.env/rasa_env/bin/activate; rasa run --log-file logs/action-server.log actions --actions actions)\n
In the $(pwd)/production/rasa-server/rasa directory:
(source ~/.env/rasa_env/bin/activate; rasa run --log-file logs/rasa-server.log --enable-api)\n
And In the $(pwd)/production/streamlit-server/streamlit
(source ~/.env/ui_env/bin/activate; streamlit run medbot_ui.py)"
