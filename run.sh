python -m http.server --cgi &
http.server --bind 0.0.0.0 --port 8080 --folder ./files &
python api.py
