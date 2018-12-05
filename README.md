# moneypit-event-log

Used to post events to while monitoring the $pit.  

```

[POST] ./api/events

{"event_type":"WARNING","event_message": "FINAL TEST","location": "moneypitmine"}

```

Valid event types:

```
INFO
WARNING
ERROR
```

Once posted to endpoint, all events are queued for submit to Elasticsearch and Twilio (based upon config settings).

## Dependencies
>
> Recommend  `sudo apt-get update` if fresh install

- Git
   `sudo apt-get install git -y`

- Python 2 w/ pip
  `sudo apt-get install python-pip -y`
  `sudo python -m pip install --upgrade pip setuptools wheel`

- Redis Server
   `sudo apt-get install redis-server -y`

- Npm / Node
   `sudo apt-get install npm -y`
   `sudo apt-get install nodejs -y`

- Python library for Elasticsearch, Redis and Twilio
  `sudo pip install elasticsearch`
  `sudo pip install redis`
  `sudo pip install twilio`

- PHP CLI / Curl
  `sudo apt-get install php7.0-cli -y`
  `sudo apt-get install php7.0-curl -y`

- A remote or local `elasticsearch` instance to post stats to (example: https://www.elastic.co/cloud)
- A twilio account

## Install

- Clone repo `git clone https://github.com/moneypit/moneypit-event-log`

- Rename `config_sample.json` to `config.json`

- Update config as necessary.

- Enable `redis-server` service is start on reboot

`sudo systemctl enable redis-server`

- Configure node / redis to start following reboot `/etc/rc.local`

```

	#!/bin/sh -e
	#
	# rc.local
	#
	# This script is executed at the end of each multiuser runlevel.
	# Make sure that the script will "exit 0" on success or any other
	# value on error.
	#
	# In order to enable or disable this script just change the execution
	# bits.
	#
	# By default this script does nothing.

	# Print the IP address
	_IP=$(hostname -I) || true
	if [ "$_IP" ]; then
	  printf "My IP address is %s\n" "$_IP"
	fi

	# Start moneypit-event-log node app / api
	sudo /usr/bin/npm start --cwd /home/pi/moneypit-event-log --prefix /home/pi/moneypit-event-log &

	exit 0

```

- From within the `./moneypit-event-log` folder install Node dependencies

```
wget https://raw.githubusercontent.com/composer/getcomposer.org/1b137f8bf6db3e79a38a5bc45324414a6b1f9df2/web/installer -O - -q | php -- --quiet
php composer.phar install
npm install

```

- Edit the `./moneypit-event-log/.env` file to set port that ui / api will listen on

```

  PORT=3000

```

- Setup the following cron jobs:

```
* * * * * python /home/pi/moneypit-event-log/scripts/post-to-es.py /home/pi/moneypit-event-log/config.json
* * * * * python /home/pi/moneypit-event-log/scripts/post-to-twilio.py /home/pi/moneypit-event-log/config.json
```

- Reboot the device to start processes

```
sudo reboot
```

## UI

`http://[hostname]:3000/`

## APIs

`GET /api/` => Swagger docs

`GET /api/events` => Returns historical list of events stored on device

`POST /api/events` => Submits events to be stored on device and fwded to Elasticsearch / Twilio
# moneypit-event-log
