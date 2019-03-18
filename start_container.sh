#!/bin/bash

#----------------------------------
# Important Settings
#----------------------------------

if [ -z "$ABI_SERVICES_CONTACT_MAIL" ]
then
  contact_email="abi-services@informatik.uni-tuebingen.de"
else
  contact_email="$ABI_SERVICES_CONTACT_MAIL"
fi

if [ -z "$ABI_SERVICES_IMPRINT_URL" ]
then
  imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
else
  imprint_url="$ABI_SERVICES_IMPRINT_URL"
fi

if [ -z "$ABI_SERVICES_GDPR_URL" ]
then
  gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"
else
  gdpr_url="$ABI_SERVICES_GDPR_URL"
fi

if [ -z "$ABI_SERVICES_SHERLOC2_MAX_SEQ" ]
then
  sherloc2_max_seq="25"
else
  sherloc2_max_seq="$ABI_SERVICES_SHERLOC2_MAX_SEQ"
fi

if [ -z "$ABI_SERVICES_SHERLOC2_PORT" ]
then
  sherloc2_port="28030"
else
  sherloc2_port="$ABI_SERVICES_SHERLOC2_PORT"
fi


#----------------------------------
# Start SherLoc2 Daemon Containers
#----------------------------------

# Without an InterProScan installation remove the volume mount flag

docker run --rm -it -d -p $sherloc2_port:80 \
           -e SL_CONTACT_EMAIL="$contact_email" \
           -e SL_IMPRINT_URL="$imprint_url" \
           -e SL_GDPR_URL="$gdpr_url" \
           -e SL_MAX_SEQ="$sherloc2_max_seq" \
           -v /local/abi_webservices/interproscan-5.29-68.0:/interproscan \
           --name abi_webservice_sherloc2 sherloc2
