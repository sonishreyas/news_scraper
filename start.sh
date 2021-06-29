if [[ -d venv ]]; then
  echo "venv already exits..."
  . venv/bin/activate
else
  echo "venv not setup, creating..."
  python3 -m venv venv
  . venv/bin/activate
  # if dependencies not installed
  # pip3 install -r requirements.txt
fi

export PYTHONPATH=$PWD

export SESSION_WINDOW_IN_SECONDS=10
export MAX_REQUEST=10
export MONGO_IP=35.224.96.28
export MONGO_PORT=27017
export MONGO_DATABASE_AUTHENTICATION=admin
export MONGO_DATABASE=news
export MONGO_USER=ripple_team
export MONGO_PWD=ripple_news_database
#export TF_CPP_MIN_LOG_LEVEL=3

python3 src/main.py -id 2 -script_id 1 -article_url https://www.hindustantimes.com/entertainment/web-series/the-family-man-actor-darshan-kumaar-says-some-fans-are-abusing-him-think-he-s-pakistani-like-his-character-101624953645520.html

#mongo -u ripple_team -p ripple_news_database --authenticationDatabase admin
