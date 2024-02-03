from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    # Assuming the input file is sent as form data
    input_file = request.files['file']
    # Process the file or data as needed
    # Example: read the file content
    file_content = input_file.read().decode('utf-8')
    # Your processing logic here, you can call another Python script or function

    # Example: returning the processed content as JSON
    output_data = {"Type": type(file_content)}
    return jsonify(output_data)

if __name__ == '__main__':
    app.run(debug=True)
