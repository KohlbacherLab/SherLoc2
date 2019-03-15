#!/bin/bash

#----------------------------------
# Start SherLoc2 Daemon Containers
#----------------------------------

contact_email="abi-services@informatik.uni-tuebingen.de"
imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"

docker run --rm -it -d -p 28030:80 \
           -e SL_CONTACT_EMAIL="$contact_email" \
           -e SL_IMPRINT_URL="$imprint_url" \
           -e SL_GDPR_URL="$gdpr_url" \
           -v /local/abi_webservices/interproscan-5.29-68.0:/interproscan \
           --name abi_webservice_sherloc2 sherloc2
