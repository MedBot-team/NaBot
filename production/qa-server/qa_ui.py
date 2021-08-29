import streamlit as st
from utils import QuestionAnswering

st.set_page_config(page_title='QuestionAnswering',
                   layout='wide', initial_sidebar_state='auto')

sample_context = """Use acetaminophen exactly as directed on the label, or as prescribed by your doctor. Do not use in larger or smaller amounts or for longer than recommended.
Do not take more of this medication than is recommended. An overdose of acetaminophen can damage your liver or cause death.
Adults and teenagers who weigh at least 110 pounds (50 kilograms): Do not take more than 1000 milligrams (mg) at one time. Do not take more than 4000 mg in 24 hours.
Children younger than 12 years old: Do not take more than 5 doses of acetaminophen in 24 hours. Use only the number of milligrams per dose that is recommended for the child's weight and age. Use exactly as directed on the label.
Avoid also using other medicines that contain acetaminophen, or you could have a fatal overdose.
If you are treating a child, use a pediatric form of acetaminophen. Use only the special dose-measuring dropper or oral syringe that comes with the specific pediatric form you are using. Carefully follow the dosing directions on the medicine label.
Measure liquid medicinewith the dosing syringe provided, or with a special dose-measuring spoon or medicine cup. If you do not have a dose-measuring device, ask your pharmacist for one.
Acetaminophen made for infants is available in two different dose concentrations, and each concentration comes with its own medicine dropper or oral syringe. These dosing devices are not equal between the different concentrations. Using the wrong device may cause you to give your child an overdose of acetaminophen. Never mix and match dosing devices between infant formulations of acetaminophen.
You may need to shake the liquid before each use. Follow the directions on the medicine label."""

sample_question = "Can you give me dosage information of Acetaminophen for children?"


def main():
    qa = QuestionAnswering()

    st.title("Transformer-based Question Answering")

    models = qa.available_model()

    model_name = st.sidebar.selectbox(
        "Choose a question answering model", models)

    qa.model_init(model_name)

    with st.form(key='qa'):
        context = st.text_area(
            "Enter text context",
            sample_context,
            height=400,
            max_chars=3000,
        )

        question = st.text_area(
            "Enter your question",
            sample_question,
            height=80,
            max_chars=500,
        )

        if st.form_submit_button("Give me the answer"):
            st.markdown("**Answer:**")

            with st.spinner("Interpreting your text (This may take some time)"):
                answer = qa.get_answer(question, context)

            st.markdown(answer)


if __name__ == "__main__":
    main()
