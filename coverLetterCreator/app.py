'''from flask import Flask, render_template, request, jsonify
from main import gpt

app = Flask(__name__, static_folder='UI/static', template_folder='UI')

@app.route('/')
def index():
    return render_template('index.html')  # Loads the HTML page

@app.route('/submit', methods=['POST'])
def submit():
    print("submit button was clicked")
    # Get the textarea values from the request
    field1_text = request.form.get('field1')
    field2_text = request.form.get('field2')
    field3_text = request.form.get('field3')
    field1_text = field1_text.replace("\r","").rstrip("\n")
    field2_text = field2_text.replace("\r","").rstrip("\n")
    field3_text = field3_text.replace("\r","").rstrip("\n")
    field1_text = field1_text.replace("\n"," \n ")
    field2_text = field2_text.replace("\n"," \n ")
    field3_text = field3_text.replace("\n"," \n ")

    # Assign them to Python variables
    text_data = {"field1": field1_text,"field2": field2_text,"field3": field3_text}

    instance = gpt(resume=field1_text, jobDescription=field2_text, additionalNotes=field3_text)
    gptResponse = instance.talkToGPT()
    return jsonify(result=gptResponse)

if __name__ == '__main__':
    app.run(debug=True)





    #print(f"*******************************************************************************************************\n\n\n\nGPT RESPONSE: {gptResponse}")

    '''