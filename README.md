a bit of fun playing with simpleaichat - https://github.com/minimaxir/simpleaichat

choose a character to talk to and save your sessions to a text file

steps:

1. get an openai account..https://platform.openai.com/

2. once you have an openai account and are logged in, you can find the option for API keys in the Personal menu at the top-right of the webpage

3. mkdir godschat

cd godschat

python3 -m venv venv
or: python -m venv venv

source venv/bin/activate
in Windows: venv\Scripts\activate

pip install simpleaichat

git clone https://github.com/stOneskull/godschat.git

add a line to your ~/.bashrc file:
export OPENAI_API_KEY=put_your_key_here

in Windows: setx OPENAI_API_KEY put_your_key_here

cd godschat
python godschat.py

deactivate