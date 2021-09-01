import requests
import streamlit as st
from decouple import config
from utils import QuestionAnswering
from ui_annotator import HTMLAnnotator


# Read API key, Rest API host address, and Rest API port from .env file
api_key = config('REST_API_KEY')
rest_host = config('REST_HOST')
rest_port = config('REST_PORT')

# Configure the web page
st.set_page_config(page_title='QuestionAnswering',
                   layout='wide',
                   initial_sidebar_state='auto')

html_annotator = HTMLAnnotator()
text_annotator = html_annotator.annotated_text

#############################
# An example of context
sample_context = """Use acetaminophen exactly as directed on the label, or as prescribed by your doctor. Do not use in larger or smaller amounts or for longer than recommended.
Do not take more of this medication than is recommended. An overdose of acetaminophen can damage your liver or cause death.
Adults and teenagers who weigh at least 110 pounds (50 kilograms): Do not take more than 1000 milligrams (mg) at one time. Do not take more than 4000 mg in 24 hours.
Children younger than 12 years old: Do not take more than 5 doses of acetaminophen in 24 hours. Use only the number of milligrams per dose that is recommended for the child's weight and age. Use exactly as directed on the label.
Avoid also using other medicines that contain acetaminophen, or you could have a fatal overdose.
If you are treating a child, use a pediatric form of acetaminophen. Use only the special dose-measuring dropper or oral syringe that comes with the specific pediatric form you are using. Carefully follow the dosing directions on the medicine label.
Measure liquid medicine with the dosing syringe provided, or with a special dose-measuring spoon or medicine cup. If you do not have a dose-measuring device, ask your pharmacist for one.
Acetaminophen made for infants is available in two different dose concentrations, and each concentration comes with its own medicine dropper or oral syringe. These dosing devices are not equal between the different concentrations. Using the wrong device may cause you to give your child an overdose of acetaminophen. Never mix and match dosing devices between infant formulations of acetaminophen.
You may need to shake the liquid before each use. Follow the directions on the medicine label."""
# An example of question
sample_question = "Can you give me dosage information of Acetaminophen for children?"

#############################


def main():
    qa = QuestionAnswering()
    # Set page title
    st.title("Transformer-based Question Answering")
    # Get the list of all available models for QA task
    models = qa.available_model()
    # Show the list of all available models in the sidebar
    model_name = st.sidebar.selectbox(
        "Choose a question answering model", models)
    # Put model change button in the form to avoid auto refresh with any change in the model_name list
    with st.sidebar.form(key='model'):
        # If change model button pressed, send a post request to the QA REST API
        if st.form_submit_button("Change model"):
            #  send a post request to the QA REST API
            _ = requests.post(f'{rest_host}:{rest_port}/model',
                              json={"model": model_name, "api_key": api_key})
    # Put context, question test areas and Give me the answer button in the form, to avoid autorefresh with any change in text areas
    with st.form(key='qa'):
        # Context text area
        context = st.text_area(
            "Enter text context",
            sample_context,
            height=400,
            max_chars=3000,
        )
        # Question text area
        question = st.text_area(
            "Enter your question",
            sample_question,
            height=80,
            max_chars=500,
        )
        # Send a post request to the QA REST API for getting the answer text
        if st.form_submit_button("Give me the answer"):
            st.markdown("**Answer:**")
            # Show this loading message
            with st.spinner("Interpreting your text (This may take some time)"):
                response = requests.post(f'{rest_host}:{rest_port}/',
                                       json={"context": context, "question": question, "api_key": api_key}).json()
            # Show the context to the user with highlighting the answer
            text_annotator(
                response['context_preceding_answer'],
                (response['answer'], "#afa"),
                response['context_following_answer'],
            )

            # st.markdown(answer)


if __name__ == "__main__":
    main()
