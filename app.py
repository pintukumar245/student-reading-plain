from flask import Flask, render_template, request
import numpy as np
import joblib
# from tensorflow.keras.models import load_model

# -------------------------
# Load model + preprocessors
# -------------------------
model = joblib.load("scaler1.joblib")      # Keras model
encoders = joblib.load("scaler3.joblib")         # dict of LabelEncoders saved during training
scaler = joblib.load("scaler2.joblib")             # StandardScaler saved during training

# Original column names used in training
catg_col = ["Level", "Class_Year", "Course_Stream", "Subject", "Preferred_Study_Time"]
numb_col = ["Syllabus_Length", "Difficulty_Level", "Hours_Available_Per_Day", "Days_Left"]

app = Flask(__name__)

# Mapping: HTML form field name -> original encoder key
FORM_TO_COL = {
    "Level": "Level",
    "Class_Year": "Class_Year",
    "Course_Stream": "Course_Stream",
    "Subject": "Subject",
    "Preferred_Study_Time": "Preferred_Study_Time"
}

def get_dropdown_options():
    """
    Return dict: { form_field_name: list_of_options }
    options are read from encoders[col].classes_ (string values)
    """
    opts = {}
    for form_name, col in FORM_TO_COL.items():
        le = encoders.get(col)
        if le is not None and hasattr(le, "classes_"):
            # convert to Python list of strings
            opts[form_name] = [str(x) for x in le.classes_]
        else:
            opts[form_name] = []
    return opts

def preprocess_input_from_form(form):
    """
    form: ImmutableMultiDict from request.form
    returns: dict ready for Keras model: { "<col>_in": array([...]), "num_input": scaled_array }
    """
    # categorical values - convert back to label encoded ints
    s_cat = []
    for form_name, col in FORM_TO_COL.items():
        raw_val = form.get(form_name, "")
        le = encoders.get(col)
        if le is not None:
            try:
                # transform will raise if unseen; we catch and map to 0
                encoded = le.transform([str(raw_val)])[0]
            except Exception:
                encoded = 0
        else:
            encoded = 0
        s_cat.append(np.array([int(encoded)], dtype=np.int32))

    # numeric values
    s_num = []
    for n in numb_col:
        v = form.get(n, "")
        try:
            fv = float(v)
        except:
            fv = 0.0
        s_num.append(fv)
    s_num = np.array([s_num], dtype=np.float32)
    s_num = scaler.transform(s_num)

    # build input dict matching model input names ("<col>_in")
    inp = {}
    for i, col in enumerate(catg_col):
        inp[f"{col}_in"] = s_cat[i]
    inp["num_input"] = s_num
    return inp

@app.route("/", methods=["GET", "POST"])
def index():
    options = get_dropdown_options()
    if request.method == "POST":
        # preprocess
        inp = preprocess_input_from_form(request.form)
        # predict
        pred = model.predict(inp)
        pred_hours = round(float(pred[0][0]), 2)
        return render_template("result.html", prediction=pred_hours)
    return render_template("index.html", options=options)

if __name__ == "__main__":
    app.run(debug=True)