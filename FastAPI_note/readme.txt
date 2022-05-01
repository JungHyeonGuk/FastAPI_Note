pip install fastapi
pip install "uvicorn[standard]"
pip install jinja2
pip install python-multipart

main.py에서
uvicorn main:app --reload 로 웹 서버 실행
uvicorn main:app --reload --port=8000 로 원하는 포트로 웹 서버 실행