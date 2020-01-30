#!/bin/sh

# This is an installation script for GEIC GWA v2.0.23
# running on Ubuntu VIrtual Machine.

# Execute as root user

# Step 1: remove old agent files from /root
rm -r /root/20191024_agent_delivery /root/geic-gwa
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

