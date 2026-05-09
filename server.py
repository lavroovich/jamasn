"""
- mini-http server
- that's all
"""
from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)

def get(ip):
    cached = False

    result = subprocess.run(
        [sys.executable, "main.py", ip],
        capture_output=True,
        text=True,
        timeout=5
    )

    code = result.returncode
    allGood = result.returncode == 0
    stderr_lines = result.stderr.strip().splitlines()

    if stderr_lines:
        last_stderr = stderr_lines[-1]
        if last_stderr == "cached":
            cached = True
        
    return result.stdout.strip(), cached, allGood, code


@app.route('/')
def route():
    ip = request.args.get('ip')

    disp, isCache, cool, code = get(ip)

    return jsonify({
        "cool": cool,
        "displayData": disp,
        "cached": isCache,
        "returncode": code
    })
    
if __name__ == "__main__":
    app.run()