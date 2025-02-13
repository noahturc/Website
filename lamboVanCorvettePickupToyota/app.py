print('hi app')
from flask import Flask, request, send_from_directory, send_file, jsonify, render_template, Blueprint
import os
import sys
from makePredictions import makePrediction


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# Create a blueprint for the cover letter creator.
cover_letter_bp = Blueprint(
    'cover_letter', __name__,
    template_folder='../coverLetterCreator/UI',      # Points to cover letter UI templates
    static_folder='../coverLetterCreator/UI/static'    # Points to cover letter UI static files
)

# Define routes on the blueprint.
@cover_letter_bp.route('/')
def CLG_index():
    # This will load ../coverLetterCreator/UI/index.html
    return render_template('index.html')

@cover_letter_bp.route('/submit', methods=['POST'])
def submit():
    try:
        print("submit button was clicked")
        # Retrieve values from the request
        field1_text = request.form.get('field1')
        field2_text = request.form.get('field2')
        field3_text = request.form.get('field3')
        
        # Clean the text inputs
        field1_text = field1_text.replace("\r", "").rstrip("\n")
        field2_text = field2_text.replace("\r", "").rstrip("\n")
        field3_text = field3_text.replace("\r", "").rstrip("\n")
        field1_text = field1_text.replace("\n", " \n ")
        field2_text = field2_text.replace("\n", " \n ")
        field3_text = field3_text.replace("\n", " \n ")

        # Create an instance of your GPT helper and get the response
        from coverLetterCreator.main import gpt
        instance = gpt(resume=field1_text, jobDescription=field2_text, additionalNotes=field3_text)
        gptResponse = instance.talkToGPT()
        return jsonify(result=gptResponse)
    except Exception as e:
        app.logger.error("Error in /submit endpoint: %s", e)
        return jsonify(error="Internal server error"), 500


app.register_blueprint(cover_letter_bp, url_prefix='/cover-letter')



@app.route("/resume")
def serve_resume():
    # serve_from_directory needs a directory and a filename
    return send_from_directory(os.path.dirname(__file__), "resume.pdf")


@app.route('/health')
def health_check():
    return "OK", 200


#########################
# from chatgpt to stop error on aws
@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.path}")
#########################





from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)


# Webhook route for Dialogflow
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return "This is the webhook endpoint. Use POST to send data.", 200

    if request.method == 'POST':
        req = request.get_json()

        # Extract intent name
        intent_name = req.get('queryResult').get('intent').get('displayName')

        # Fulfillment response
        if intent_name == "testing":  # Replace with your intent name
            return jsonify({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["test text 1"]
                        }
                    },
                    {
                        "text": {
                            "text": ["test text 2"]
                        }
                    }
                ]
            })
        else:
            return jsonify({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["Sorry, I can't handle that intent."]
                        }
                    }
                ]
            })

@app.route('/')
def index():
    # Serve the index.html file
    file_path = os.path.join(BASE_DIR, 'index.html')
    return send_file(file_path)

@app.route('/<path:filename>')
def serve_static_files(filename):
    # Serve any other file (CSS, JS, etc.)
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404

# Route to serve the HTML page
@app.route('/index2')
def index2():
    print('hi index2 fn')
    return send_from_directory('', 'index2.html')  # Ensure 'index2.html' is in the same directory as your Python script

# Route to handle the image upload and processing
@app.route('/run-script', methods=['POST'])
def run_script():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image = request.files['image']

    prediction, confidenceList = makePrediction(image=image)
    result = 'Nothing'

    if prediction == 'corvetteStingray':
        result = '''Prediction: Corvette Stingray
        
Average Price:
Starting at around $65,000 to $85,000 depending on options and packages.

Engine Specifications:
6.2L V8 engine, producing 490 to 495 horsepower.

Fuel Efficiency:
15-27 MPG (City/Highway)

Seating Capacity:
2 passengers.

Cargo Space:
12.6 cubic feet of cargo space (front and rear trunks combined).'''


    elif prediction == 'fordPickupTruck':
        result = '''Prediction: Ford Pickup Truck

Average Price:
Starting at around $35,000 to $85,000 depending on trim, engine, and options.

Engine Specifications:
3.3L V6, 2.7L EcoBoost V6, 5.0L V8, and a 3.5L PowerBoost hybrid are common options, with horsepower ranging from 290 to 450+.

Fuel Efficiency:
19-25 MPG (City/Highway), varies based on engine type.

Seating Capacity:
Up to 6 passengers (depending on cab configuration).

Cargo Space:

Bed lengths: 5.5 ft, 6.5 ft, or 8 ft depending on the model and cab configuration.'''


    elif prediction == 'hondaOdyssey':
        result = '''Prediction: Honda Odyssey

Average Price:
Starting at around $37,000 to $50,000 depending on trim and options.

Engine Specifications:
3.5L V6 engine, producing 280 horsepower.

Fuel Efficiency:
19-28 MPG (City/Highway)

Seating Capacity:
7-8 passengers, depending on the model.

Cargo Space:
Up to 158 cubic feet with the second and third rows folded.'''


    elif prediction == 'lamborghini':
        result = '''Prediction: Lamborghini
        
Average Price:
Starting at around $200,000 to over $500,000 depending on the model and customization.

Engine Specifications:
Huracán: 5.2L V10 engine, producing 602-631 horsepower.
Aventador: 6.5L V12 engine, producing 730-770 horsepower.

Fuel Efficiency:
10-19 MPG (City/Highway), varies by model.

Seating Capacity:
2 passengers.

Cargo Space:
About 3.5 cubic feet (limited due to supercar design).'''


    elif prediction == 'toyotaRAV4':
        result = '''Prediction: Toyota RAV 4

Average Price:
Starting at around $28,000 to $40,000 depending on the trim level and options.

Engine Specifications:
2.5L 4-cylinder engine, producing 203 horsepower. Hybrid and plug-in hybrid variants are also available.

Fuel Efficiency:
27-35 MPG (City/Highway) depending on the model (higher for hybrids).

Seating Capacity:
5 passengers.

Cargo Space:
Up to 69.8 cubic feet with the rear seats folded.'''

    else:
        result = 'error line 192'
        return result

    print(f'hi run script fn\nConfidence List is: {confidenceList}')
    x = f'{result}\n\n\nConfidence:\n{confidenceList[0]}'
    return x

print('end of app')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)