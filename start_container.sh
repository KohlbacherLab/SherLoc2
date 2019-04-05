#!/bin/bash

#----------------------------------
# Important Settings
#----------------------------------

# Enter a valid eMail address that allows to contact the responsible colleague for this webservice
if [ -z "$ABI_SERVICES_CONTACT_MAIL" ]
then
  contact_email="abi-services@informatik.uni-tuebingen.de"
else
  contact_email="$ABI_SERVICES_CONTACT_MAIL"
fi

# Enter a valid URL that leads to the appropriate imprint page
if [ -z "$ABI_SERVICES_IMPRINT_URL" ]
then
  imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
else
  imprint_url="$ABI_SERVICES_IMPRINT_URL"
fi

# Enter a valid URL that leads to the appropriate GDPR declaration page
if [ -z "$ABI_SERVICES_GDPR_URL" ]
then
  gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"
else
  gdpr_url="$ABI_SERVICES_GDPR_URL"
fi

# Here you can set an upper limit for the number of sequences allowed to be submitted
if [ -z "$ABI_SERVICES_SHERLOC2_MAX_SEQ" ]
then
  sherloc2_max_seq="25"
else
  sherloc2_max_seq="$ABI_SERVICES_SHERLOC2_MAX_SEQ"
fi

# Here you can specify th host port that is bound to port 80 from the container
if [ -z "$ABI_SERVICES_SHERLOC2_PORT" ]
then
  sherloc2_port="28030"
else
  sherloc2_port="$ABI_SERVICES_SHERLOC2_PORT"
fi

#----------------------------------
# Start SherLoc2 Daemon Containers
#----------------------------------

if [ -z "$INTERPROSCAN_LOCAL" ]
then
  docker run --rm -it -d -p $sherloc2_port:80 \
             -e SL_CONTACT_EMAIL="$contact_email" \
             -e SL_IMPRINT_URL="$imprint_url" \
             -e SL_GDPR_URL="$gdpr_url" \
             -e SL_MAX_SEQ="$sherloc2_max_seq" \
             --name abi_webservice_sherloc2 sherloc2
else
  docker run --rm -it -d -p $sherloc2_port:80 \
             -e SL_CONTACT_EMAIL="$contact_email" \
             -e SL_IMPRINT_URL="$imprint_url" \
             -e SL_GDPR_URL="$gdpr_url" \
             -e SL_MAX_SEQ="$sherloc2_max_seq" \
             -v $INTERPROSCAN_LOCAL:/interproscan \
             --name abi_webservice_sherloc2 sherloc2
fi
