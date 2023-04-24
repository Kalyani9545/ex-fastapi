FROM Python 3.11.2
WORKDIR /ProgramData/Microsoft/Windows/Start Menu/Programs
COPY requirements.txt ./
RUN pip install --no-cache-dir  -r requirements.txt

COPY ..

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
