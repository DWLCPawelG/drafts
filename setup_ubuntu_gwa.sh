#!/bin/sh

# This is an installation script for GEIC GWA v2.0.23
# running on Ubuntu VIrtual Machine.

# Execute as root user

# Step 1: remove old agent files from /root
rm -r /root/20191024_agent_delivery /root/geic-gwa

# Step 2: copy latest agent image from Alpha to /root dir and unzip it there:
LATEST=`ls -at /mnt/Archive/\!Projects/GE_Current_phase2/ | head -n 1`
cp -r /mnt/Archive/\!Projects/GE_Current_phase2/$LATEST/*.zip /root/ && unzip /root/*.zip -d /root

# Step 3: configure Agenti
sed -i "s/\"clean_session\":false/\"clean_session\":true/g"
read -p "httpgw_url: " HTTPGW_URL
sed -i "s/httpgwgeic-stage.proximetry.com/$HTTPGW_URL/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
read -p "httpgw_port [443]: " HTTPGW_PORT
HTTPGW_PORT=${HTTPGW_PORT:-443}
sed -i "s/18080/$HTTPGW_PORT/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
sed -i "s/\"use_secure_conn\":\"no\"/\"use_secure_conn\":\"yes\"/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
read -p "uaa_url: " UAA_URL
sed -i "s/uaageic-stage.proximetry.com/$UAA_URL/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
read -p "uaa_user: " UAA_USER
sed -i "s/user/$UAA_USER/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
read -p "uaa_password: " UAA_PASSWORD
sed -i "s/\"uaa_password\":\"password\"/\"uaa_password\":\"$UAA_PASSWORD\"/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
read -p "node_did [ssh_test]: " NODE_DID
NODE_DID=${NODE_DID:-ssh_test}
sed  -i "s/HEALTH/$NODE_DID/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json

#sed "s/\"server_port\":\s443/\"server_port\": $PORT/g" /root/geic-gwa/gwa-pdm-cloud-adapter-config.json
