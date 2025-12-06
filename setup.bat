@echo off
echo Setting up FastAPI Backend...

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your configuration.
) else (
    echo .env file already exists.
)

echo.
echo Setup complete!
echo.
echo To run the server:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python main.py
echo   3. Or run: python run.py
echo.
pause

