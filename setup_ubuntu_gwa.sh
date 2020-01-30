#!/bin/sh

# This is an installation script for GEIC GWA v2.0.23
# running on Ubuntu VIrtual Machine.

# Execute as root user

# Step 1: remove old agent files from /root
rm -r /root/20191024_agent_delivery /root/geic-gwa 2>/dev/null 
echo


# Step 2: copy latest agent image from Alpha to /root dir and unzip it there:
LATEST=`ls -at /mnt/Archive/\!Projects/GE_Current_phase2/ | grep -i agent_delivery | head -n 1`
echo $LATEST
cp -r /mnt/Archive/\!Projects/GE_Current_phase2/$LATEST/*.zip /root/ && unzip /root/*.zip -d /root
echo


# Step 3: configure Agent:
echo "Enter the following agent configuration parameters: "
sed -i "s/\"clean_session\":false/\"clean_session\":true/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/\"clean_session\":false/\"clean_session\":true/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json
sed -i "s/\"command_request_folder\": \".\/\"/\"command_request_folder\": \"\/opt\/relayr\/commands\/command_request_folder\"/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json
sed -i "s/\"command_result_folder\": \".\/\"/\"command_result_folder\": \"\/opt\/relayr\/commands\/command_result_folder\"/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json
sed -i "s/\"command_details_folder\": \".\/\"/\"command_details_folder\": \"\/opt\/relayr\/commands\/command_details_folder\"/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json
sed -i "s/test/lampa/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json

read -p "httpgw_url: " HTTPGW_URL
sed -i "s/httpgwgeic-stage.proximetry.com/$HTTPGW_URL/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/httpgwgeic-stage.proximetry.com/$HTTPGW_URL/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json

read -p "httpgw_port [443]: " HTTPGW_PORT
HTTPGW_PORT=${HTTPGW_PORT:-443}
sed -i "s/18080/$HTTPGW_PORT/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/\"use_secure_conn\":\"no\"/\"use_secure_conn\":\"yes\"/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json

read -p "uaa_url: " UAA_URL
sed -i "s/uaageic-stage.proximetry.com/$UAA_URL/g" /root/geic-gwa/geic-gwa-pdm-cloud-adapter-config.json
sed -i "s/uaageic-stage.proximetry.com/$UAA_URL/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json

read -p "uaa_user: " UAA_USER
sed -i "s/\"uaa_user\":\"user\"/\"uaa_user\":\"$UAA_USER\"/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/\"uaa_user\":\"user\"/\"uaa_user\":\"$UAA_USER\"/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json

read -p "uaa_password: " UAA_PASSWORD
sed -i "s/\"uaa_password\":\"password\"/\"uaa_password\":\"$UAA_PASSWORD\"/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/\"uaa_password\":\"password\"/\"uaa_password\":\"$UAA_PASSWORD\"/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json

read -p "node_did [ssh_test]: " NODE_DID
NODE_DID=${NODE_DID:-ssh_test}
sed -i "s/HEALTH/$NODE_DID/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/HEALTH/$NODE_DID/g" /root/geic-gwa/geic-gwa-health-status-adapter-config.json
echo


# Step 4: install agent using script: install.sh (it will create /opt/relayr directory and "root" user & group in system)
# Core, Cloud Adapter and Package Manager should install correctly, only Health Status Adapter will not (that's expected as several important directories are missing). Agent can't run without HSA.
./root/geic-gwa/install.sh


# Step 5: create neccessary folders
mkdir -p /var/log/isap_logs \
    mkdir -p /opt/relayr/staging \
    mkdir -p /opt/relayr/results \
    mkdir -p /opt/relayr/commands/command_request_folder \
    mkdir -p /opt/relayr/commands/backup_command_request_folder \
    mkdir -p /opt/relayr/commands/command_result_folder \
    mkdir -p /opt/relayr/commands/backup_command_result_folder \
    mkdir -p /opt/relayr/commands/command_details_folder \
    mkdir -p /opt/relayr/commands/backup_command_details_folder


# Step 6: change ownership of /opt/relayr directory
chown prox:prox -R /opt/relayr


# Step 7: configure SSH Daemon on Agent host
apt update && apt install openssh-server --yes
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAjHr5zCD5U0xChCQOK7sIpQzdNamt6QPMLg9DoXAqrgtofigPtdmZI6x1SM5cIeMql4/sLF0RakXQKeRCz4KDQY0pK1X+1RpGoqnjrsehLZgDjLJYexNUDUSeJfLMkeQSYtpgVOL2IzHnPxTZAWdSyEPkUaQCvKoXsYVG3Fp4nJffKOcsxS7V3upO4mLBVZD9TeJJvGbtPGWTZEl3p40LB93heIKCqb/vvLFHhVKfwArWkWRXsuDU4Upg9mXv38jlMcdRAj8xXFLYtxrUsQhp84OPcB2HD88CupgsEsWGjPEABz6leUWJxG+0ZzN1HVGmApoDUuh3faFlir0/X7MAJw== rcs-dev.key" > /home/lampa/.ssh/authorized_keys


# Step 8: Restart Health Status Adapter
systemctl restart relayr-geic-gwa-health-status-adapter.service

echo "Your Agent should be up & running within a couple of seconds and Reachable in a couple of minutes. Have a nice day!"

