import pexpect
import time
from translate import Translator
import os
eng = Translator(from_lang="en", to_lang="ru")
rus = Translator(from_lang="ru", to_lang="en")
try:
    os.remove("ready")
    os.remove("generating")
except:
    time.sleep(0)
print("Llama.cpp (re)started")
cmd = './llama.cpp/main -m llama.cpp/models/13B/airoboros-ggml-model-q4_0.bin -n 2048 --repeat_penalty 1.0 --color -i -r "User:" -f chat-with-gab.txt'
print(cmd)
child = pexpect.spawn(cmd)
child.expect('User:')
child.expect('User:')
child.expect('User:')
time.sleep(30)
open("ready", 'a').close()
print("Llama.cpp ready")
child.expect("User:")
while True:
    while os.path.isfile("h_input.txt") == False:
        pass
    time.sleep(0.5)
    f = open("h_input.txt", "r")
    line = f.read()
    f.close()
    os.remove("h_input.txt")
    if line == "!reboot":
        child.terminate()
        try:
            os.remove("ready")
        except:
            time.sleep(0)
        print("Llama.cpp (re)started")
        print('./llama.cpp/main -m llama.cpp/models/13B/airoboros-ggml-model-q4_0.bin -n 2048 --repeat_penalty 1.0 --color -i -r "User:" -f chat-with-gab.txt')
        child = pexpect.spawn(cmd)
        child.expect('User:')
        child.expect('User:')
        child.expect('User:')
        time.sleep(30)
        open("ready", 'a').close()
        print("Llama.cpp ready")
        child.expect("User:")
        f = open("history.txt", "w")
        f.write("Rebooted")
        f.close()
    else:
        open("generating", 'a').close()
        tr_line = rus.translate(line.replace(',', ''))
        print(f'{line} - {tr_line}')
        child.sendline(tr_line)
        hist = f"User: {line}<br>-----------------<br>"
        f = open("history.txt", "r")
        older = f.read()
        f.close()
        text = hist + older
        f = open("history.txt", "w")
        f.write(text)
        f.close()

        child.expect("\n", timeout=999999)
        child.expect('User:', timeout=999999)
        output = child.before.decode("utf-8")
        output = output.replace("Gab:", "", 1)
        output = output[1:]
        response = eng.translate(output)
        response = response.replace("[0м", "")
        response = response.replace("[0m", "")
        try:
            os.remove("generating")
        except:
            time.sleep(0)
        print(f'{output} - {response}')
        hist = (f"Gab: {response}<br><br>")
        f = open("history.txt", "r")
        older = f.read()
        f.close()
        text = hist + older
        f = open("history.txt", "w")
        f.write(text)
        f.close()

