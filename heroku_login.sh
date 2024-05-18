#!/bin/bash

if [ -z "$HEROKU_API_KEY" ]; then
  echo "HEROKU_API_KEY is not set. Please set it and try again."
  exit 1
fi

echo "machine api.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_API_KEY
machine git.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_API_KEY" > ~/.netrc

chmod 600 ~/.netrc

echo "Heroku CLI configured with HEROKU_API_KEY."
