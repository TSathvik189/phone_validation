from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Replace with your actual Abstract API token
ABSTRACT_API_TOKEN = "d368ba0dd7854a5785ab973b544418ef"
API_URL = "https://phonevalidation.abstractapi.com/v1/?"

# HTML template with improved UI for the home page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phone Number Validation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            text-align: left;
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phone Number Validation</h1>
        <form id="phoneForm">
            <input type="text" name="phone" id="phone" placeholder="Enter phone number" required>
            <button type="submit">Validate</button>
        </form>
        <div id="result" class="result"></div>
    </div>

    <script>
        document.getElementById('phoneForm').addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent form from refreshing the page
            const phone = document.getElementById('phone').value;
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = ''; // Clear previous results

            try {
                const response = await fetch('/validate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ phone: phone }),
                });

                if (response.ok) {
                    const data = await response.json();
                    resultDiv.innerHTML = `
                        <p><strong>Phone:</strong> ${data.phone}</p>
                        <p><strong>Valid:</strong> ${data.valid}</p>
                        <p><strong>Formatted:</strong> ${data.format.international || 'N/A'}</p>
                        <p><strong>Country:</strong> ${data.country.name || 'N/A'}</p>
                        <p><strong>Location:</strong> ${data.location || 'N/A'}</p>
                        <p><strong>Type:</strong> ${data.type || 'N/A'}</p>
                        <p><strong>Carrier:</strong> ${data.carrier || 'N/A'}</p>
                    `;
                } else {
                    const errorData = await response.json();
                    resultDiv.innerHTML = `<p class="error">${errorData.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Renders the home page with a form for phone number validation."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/validate', methods=['POST'])
def validate_phone():
    """Validates the phone number using the Abstract API."""
    phone_number = request.form.get('phone')

    # API call to Abstract API for phone validation
    try:
        response = requests.get(API_URL, params={
            'api_key': ABSTRACT_API_TOKEN,
            'phone': phone_number
        }, timeout=10)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {e}'}), 500

    if response.status_code == 200:
        data = response.json()
        # Extract relevant fields from the response
        phone = data.get('phone', '')
        valid = data.get('valid', False)
        formatted_phone = data.get('format', {})
        country = data.get('country', {})
        location = data.get('location', '')
        phone_type = data.get('type', '')
        carrier = data.get('carrier', '')

        # Return the validation result as JSON
        return jsonify({
            'phone': phone,
            'valid': valid,
            'format': formatted_phone,
            'country': country,
            'location': location,
            'type': phone_type,
            'carrier': carrier
        })
    else:
        return jsonify({'error': 'Failed to validate phone number'}), 400

if __name__ == '__main__':
    app.run(debug=True)
