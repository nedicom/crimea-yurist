lawyer's site

My python project
Python 3.7.0 + front (html, js, css)

1. git clone https://github.com/nedicom/crimea-yurist .
2. db: create/download db.sqlite3 or connect another (dbexample.sqlite3 - trim example)
3. create environment: python -m venv myenv
4. activate virtual environment: .\myenv\Scripts\activate or source myenv/bin/activate
5. install framework and CMS: 
- pip install django==3.2.25 
- pip install wagtail==4.1.4
6. python manage.py runserver

options:
# tailwindcss install
# linux
curl -LO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss
# windows
Invoke-WebRequest -Uri "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe" -OutFile "tailwindcss-windows-x64.exe"
move tailwindcss-windows-x64.exe tailwindcss.exe

# tailwindcss usage
# linux
./tailwindcss --input ./myproject/src/style.css --output ./myproject/static/css/output.css --watch --content "./myproject/templates/**/*.html"

# windows
.\tailwindcss.exe --input .\myproject\src\style.css --output .\myproject\static\css\output.css --watch --content "./myproject/templates/**/*.html"

The best law site ever - https://crimea-yurist.ru
