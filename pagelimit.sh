#!/bin/bash

DLTIME=$(curl -v --silent http://imt3003.skyhigh.iik.ntnu.no:9001/metrics 2>&1 |grep "actual_last_download_time{name=\"Oppetid\",tags=\"imt3003\"}" | sed -n -e 's/^.*}//p')
DLTIME="${DLTIME:1}"
echo "Current download time:"
echo $DLTIME
echo ""
if (( $(echo "$DLTIME < 1" |bc -l) )); then
    echo "Less than one second"
    if [[ $LASTTIMEs -eq 1 ]]; then 
        echo "Previous record below one second"
        PAGELIMIT=$((PAGELIMIT + 25))
        docker service update --env-add BF_FRONTPAGE_LIMIT=$PAGELIMIT --with-registry-auth bf_web
        echo "Sent docker service update cmd"
    else
        echo "First record of below one second. Standing by."
    fi
    LASTITME=1
else
    echo "More than one second"
    if [[ $LASTTIME -eq 0 ]]; then
        echo "Previous record above one second."
        echo "Decreasing page limit"
        PAGELIMIT=$((PAGELIMIT - 25))
        docker service update --env-add BF_FRONTPAGE_LIMIT=$PAGELIMIT --with-registry-auth bf_web
        echo "Sent docker service update cmd"
    else
        echo "First record of above one second. Standing by."
    fi
    LASTTIME=0
fi