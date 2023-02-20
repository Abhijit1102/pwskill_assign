from flask import Flask, request

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse_string():
    input_string = request.json['input_string']
    output_string = input_string[::-1]
    return {'reversed_string': output_string}

if __name__ == '__main__':
    app.run()

