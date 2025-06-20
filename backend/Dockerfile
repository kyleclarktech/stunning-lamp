FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make initialization script executable
RUN chmod +x scripts/init_db.py

EXPOSE 8000

# Create a startup script that initializes the database and then starts the app
RUN echo -e '#!/bin/bash\npython scripts/init_db.py\nexec uvicorn main:app --host 0.0.0.0 --port 8000 --reload' > start.sh && chmod +x start.sh

CMD ["./start.sh"]