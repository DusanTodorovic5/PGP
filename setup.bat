REM Create virtual environment
python -m venv env

REM Activate virtual environment
call env\Scripts\activate

REM Install dependencies from requirements.txt
pip install -r requirements.txt