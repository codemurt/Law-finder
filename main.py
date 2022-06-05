import io

import streamlit as st

import model as md


def _hide_streamlit_menu():
    hide_menu_style = """
        <style>
        #MainMenu {visibility : hidden; }
        footer {visibility : hidden; }
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


# @st.cache
def AI_thinking(question: str, option: str):
    with st.spinner("AI thinking..."):
        return md.get_answer(option, question)


# return f'Answer: {res["answer"]}\nConfidence in the answer: {str(round(res["score"], 3))}'
# st.write("Answer: ", res['answer'])
# st.write("Confidence in the answer: ", str(round(res['score'], 3)))


def main():
    st.set_page_config(page_title="Law Finder")
    _hide_streamlit_menu()

    st.title("Law Finder - найдет все ответы.")

    option = st.selectbox(
        'Выберите законодательный акт: ',
        ('Конституция РФ', 'Федеральные законы РФ', 'Трудовой кодекс РФ', 'Собственный текст'))

    if option == "Собственный текст":
        uploaded_file = st.file_uploader(label="Загрузите сюда файл в вашим текстом", type=['txt'])
        if uploaded_file is not None:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.write(stringio.getvalue())
            st.text_area()
    else:
        form = st.form(key="FORM")
        with form:
            question = st.text_area("QUESTION:")
            submitted = st.form_submit_button(label="Get Answer")
        if submitted:
            print(question, option)
            if question == "":
                st.error("Введите вопрос!")
            if question != "":
                answer, context = AI_thinking(question, option)
                st.markdown(
                    f'### Answer: \n ### {answer["answer"]}\n Confidence in the answer: {str(round(answer["score"], 3))}')
                st.text_area(value=context, disabled=True, label="Context", height=500)


if __name__ == "__main__":
    main()
