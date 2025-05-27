Setup

With Docker (Recommended for Presentation):
powershell

Copy
cd D:\REGex\bsp
$env:DB_HOST = "db"
$env:FLASK_ENV = "production"
docker-compose up --build
Locally:
powershell

Copy
cd D:\REGex\bsp
$env:DB_HOST = "localhost"
$env:FLASK_ENV = "development"
python run.py
Access at http://localhost:5000/.