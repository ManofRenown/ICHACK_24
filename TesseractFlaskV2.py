from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_script')
def run_script():
    try:
        # Execute the Python script
        result = subprocess.run(['python', './test_server.py'], capture_output=True, text=True) #your script should be replaced with path to our script
        if result.returncode == 0:
            return 'Script executed successfully'
        else:
            return 'Error executing script: ' + result.stderr, 500
    except Exception as e:
        return 'Error: ' + str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
