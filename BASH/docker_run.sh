#! /bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")") # get the directory of this script
BUILDFILE=$SCRIPT_DIR/docker_build.sh # get the path to the docker build script

IMAGE_NAME="blast-radius-fork-local"
ACCESS_PORT=5000

# first check if number of arguments to script is greater than 3 or not, if it is exit
if [ $# -gt 3 ]; then
    echo "$0 does not accept more than 2 arguments (image name & port). You have provided $# arguments."
    exit 1
fi

# if number of arguments is equal to 0
if [ $# -eq 0 ]; then
    echo "Using default image name: ${IMAGE_NAME} and default port: ${ACCESS_PORT} because no arguments were passed"
else
    if [ "$1" != "" ]; then
        IMAGE_NAME=$1
    fi
    if [ "$2" != "" ]; then
        ACCESS_PORT=$2
    fi
fi

# check if image exists, if not try to build it
if [[ "$(docker image inspect "$IMAGE_NAME" --format='exists')" != 'exists' ]]; then
  echo "$IMAGE_NAME does not exist. Trying to build the image using $BUILDFILE ..."

  if [ ! -e "$BUILDFILE" ]; then
    echo "File $BUILDFILE does not exist. Exiting"
    exit 1
  fi

  if [ ! -s "$BUILDFILE" ]; then
    echo "File $BUILDFILE is empty. Exiting"
    exit 1
  fi

  if [ ! -x "$BUILDFILE" ]; then
    echo "File $BUILDFILE is not executable. Exiting"
    echo "Hint: Try running 'chmod +x $BUILDFILE'"
    exit 1
  fi

  echo "Using $BUILDFILE to build image $IMAGE_NAME"
  $BUILDFILE "$IMAGE_NAME"

fi

if [[ "$(docker image inspect "$IMAGE_NAME" --format='exists')" == 'exists' ]]; then
  echo "Attempting to run Docker Image: $IMAGE_NAME on $ACCESS_PORT"
  docker run --rm -it -d -p "$ACCESS_PORT":5000 \
    -v "$(PWD)":/data:ro \
    --security-opt apparmor:unconfined \
    --cap-add=SYS_ADMIN \
    "$IMAGE_NAME"
fi