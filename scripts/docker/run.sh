#!/bin/bash

if [ -n "$SSH_AUTH_SOCK" ]; then
    # ssh agent is running
    ADDITIONAL_ARGS="$ADDITIONAL_ARGS -v $SSH_AUTH_SOCK:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent"
fi

TZ="$(timedatectl show --property=Timezone | cut -d'=' -f2)"
echo "Passed timezone to docker: $TZ"

docker run \
    -e TZ=$TZ \
    --privileged --rm -it \
    -v ".:/mnt/ratatai" \
    -v "/tmp/tmux-1000":"/mnt/tmp-tmux-1000/" \
    --network=host \
    $ADDITIONAL_ARGS \
    ratatai:latest \
    bash
