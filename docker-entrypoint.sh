#!/bin/sh
set -e

# If command starts with an option, prepend blast-radius so Docker users can run
# `docker run image --serve ...` as shorthand.
if [ "${1#-}" != "${1}" ]; then
  set -- blast-radius "$@"
elif [ "${1}" != "blast-radius" ]; then
  if [ -n "${1}" ]; then
    set -- blast-radius "$@"
  fi
fi

# Assert CLI args are overwritten, otherwise set them to preferred defaults.
export TF_CLI_ARGS_get=${TF_CLI_ARGS_get:-'-update'}
export TF_CLI_ARGS_init=${TF_CLI_ARGS_init:-'-input=false'}

# Inside the container
# Need to create the upper and work dirs inside a tmpfs.
# Otherwise OverlayFS complains about AUFS folders.
# Source: https://gist.github.com/detunized/7c8fc4c37b49c5475e68ef9574587eee
mkdir -p /tmp/overlay && \
mount -t tmpfs tmpfs /tmp/overlay && \
mkdir -p /tmp/overlay/upper && \
mkdir -p /tmp/overlay/work && \
mkdir -p /data-rw && \
mount -t overlay overlay -o lowerdir=/data,upperdir=/tmp/overlay/upper,workdir=/tmp/overlay/work /data-rw

# change to the overlayFS
cd /data-rw

# Is Terraform already initialized? Ensure modules are all downloaded.
[ -d '.terraform' ] && terraform get

# Initialize Terraform with the version embedded in this Docker image.
if [ -n "$CHDIR" ] && [ -d "$CHDIR" ]; then
  echo "Initializing Terraform in directory: $CHDIR"
  terraform -chdir="$CHDIR" init
else
  echo "Initializing Terraform in directory: /data-rw"
  terraform init
fi

# it's possible that we're in a sub-directory. leave.
cd /data-rw

# Let's go!
exec "$@"
