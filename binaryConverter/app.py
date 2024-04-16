from flask import Flask, render_template, request
from flask_frozen import Freezer
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    error = None
    if request.method == 'POST':
        if 'convert_to_binary' in request.form:
            text = request.form['text']
            result = text_to_binary(text)
        elif 'convert_to_text' in request.form:
            binary = request.form['binary']
            result = binary_to_text(binary)
        
        # Check if the result contains 'Error'
        if "Error" in result:
            error = result
            result = ""

    return render_template('index.html', result=result, error=error)


def text_to_binary(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def binary_to_text(binary, encoding='utf-8', errors='surrogatepass'):
    try:
        # Clean the input by removing spaces
        binary = ''.join(binary.split())
        
        # Check if binary is valid (contains only 0 and 1)
        if not all(c in '01' for c in binary):
            return "Error: Binary input should contain only 0s and 1s."
        
        # Convert binary to text
        n = int(binary, 2)
        text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors)
        return text if text else "Error: No text representation."
    except ValueError as e:
        return "Error: Invalid binary number."
    except Exception as e:
        return f"Error: {str(e)}"

freezer = Freezer(app)
# if __name__ == "__main__":
#     app.run()
if __name__ == '__main__':
    # Generate the static files using Frozen-Flask
    freezer.freeze()
