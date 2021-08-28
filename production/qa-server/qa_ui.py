import logging
import os

import streamlit as st
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
from transformers import pipeline


os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)


@st.cache(allow_output_mutation=True, suppress_st_warning=True, max_entries=1)
def load_model(model_name):
    return (
        TFAutoModelForQuestionAnswering.from_pretrained(model_name),
        AutoTokenizer.from_pretrained(model_name),
    )


def main():

    st.title("Transformer-based Question Answering Demo App")

    models = [
        "bert-large-uncased-whole-word-masking-finetuned-squad",
        "bert-large-cased-whole-word-masking-finetuned-squad",
        "distilbert-base-uncased-distilled-squad",
        "distilbert-base-cased-distilled-squad",
        "allenai/longformer-large-4096-finetuned-triviaqa" ]

    model_name = st.sidebar.selectbox(
        "Choose a question answering model", models
    )

    model, tokenizer = load_model(model_name)

    
    context = st.text_area(
        "Enter text context",
        """Use acetaminophen exactly as directed on the label, or as prescribed by your doctor. Do not use in larger or smaller amounts or for longer than recommended.
Do not take more of this medication than is recommended. An overdose of acetaminophen can damage your liver or cause death.
Adults and teenagers who weigh at least 110 pounds (50 kilograms): Do not take more than 1000 milligrams (mg) at one time. Do not take more than 4000 mg in 24 hours.
Children younger than 12 years old: Do not take more than 5 doses of acetaminophen in 24 hours. Use only the number of milligrams per dose that is recommended for the child's weight and age. Use exactly as directed on the label.
Avoid also using other medicines that contain acetaminophen, or you could have a fatal overdose.
If you are treating a child, use a pediatric form of acetaminophen. Use only the special dose-measuring dropper or oral syringe that comes with the specific pediatric form you are using. Carefully follow the dosing directions on the medicine label.
Measure liquid medicinewith the dosing syringe provided, or with a special dose-measuring spoon or medicine cup. If you do not have a dose-measuring device, ask your pharmacist for one.
Acetaminophen made for infants is available in two different dose concentrations, and each concentration comes with its own medicine dropper or oral syringe. These dosing devices are not equal between the different concentrations. Using the wrong device may cause you to give your child an overdose of acetaminophen. Never mix and match dosing devices between infant formulations of acetaminophen.
You may need to shake the liquid before each use. Follow the directions on the medicine label.""",
        height=400,
        max_chars=3000,
    )

    question = st.text_area(
        "Enter your question",
        "Can you give me dosage information of Acetaminophen for children?",
        height=100,
        max_chars=500,
    )


    if st.button("Interpret Text"):

        st.text("Output")
        with st.spinner("Interpreting your text (This may take some time)"):
            inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="tf")
            input_ids = inputs["input_ids"].numpy()[0]

            answer_start_scores, answer_end_scores = model(inputs, return_dict=False)

            answer_start = tf.argmax(
                                    answer_start_scores, axis=1
                                    ).numpy()[0] 
            answer_end = (
                        tf.argmax(answer_end_scores, axis=1) + 1
                        ).numpy()[0]  

            answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        st.text(answer)


if __name__ == "__main__":
    main()