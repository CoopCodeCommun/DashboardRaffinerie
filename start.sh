#curl -sSL https://install.python-poetry.org | python3
export PATH="/home/pilot/.local/bin:$PATH"
poetry install
echo "Poetry install ok"

poetry run python3 manage.py migrate
poetry run python3 manage.py popdb

poetry run python3 manage.py runserver 0.0.0.0:8080

#echo "sleep infinity"
#sleep infinity

