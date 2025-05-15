https://cmake.org/download/
https://visualstudio.microsoft.com/visual-cpp-build-tools/
./venv/Scripts/pip install -r requirements.txt
cd Backend
../venv/Scripts/python.exe manage.py makemigrations
../venv/Scripts/python.exe manage.py migrate
../venv/Scripts/python.exe manage.py runserver
cd face-login
npm install
npm run dev
