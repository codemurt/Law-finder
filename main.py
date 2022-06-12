import io

import streamlit as st
from annotated_text import annotation

import PDFExtractor as pdfe
import doc_file_worker
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


def main():
    st.set_page_config(page_title="Law Finder")
    _hide_streamlit_menu()

    st.title("Law Finder - найдет все ответы.")

    option = st.selectbox(
        'Выберите законодательный акт: ',
        doc_file_worker.get_doc_files())

    if option == "Собственный текст":
        form = st.form(key="FORM")
        with form:
            doc_name = st.text_input("Введите название документа")
            uploaded_file = st.file_uploader(label="Загрузите сюда файл в вашим текстом", type=['txt', 'pdf'])
            submitted = st.form_submit_button(label="Upload file")

        if submitted:
            if uploaded_file is not None:
                print(uploaded_file.type)
                if uploaded_file.type == 'application/pdf':
                    text = pdfe.extract_text(uploaded_file)
                    print(text)
                else:
                    text = io.StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue()
                if doc_file_worker.add_file(doc_name, uploaded_file.name, text):
                    st.info("Документ успешно сохранен")
                    st.write(text[:len(text) % 1000] + ".....")
                else:
                    st.error("Документ с таким название уже существует")
            else:
                st.error("Не указан файл")
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
                answer_str = answer['answer']
                st.write("## Correct answer")
                st.write("# " + answer_str)
                st.write(f'Confidence in the answer: {str(round(answer["score"], 3))}')

                start_idx = context.find(answer_str)
                end_idx = start_idx + len(answer_str)

                st.write("## Context")
                st.markdown(
                    context[:start_idx] + str(annotation(answer_str, "ANSWER", "#8ef")) + context[end_idx:],
                    unsafe_allow_html=True)

                # st.markdown(
                # f'### Answer: \n ### {answer["answer"]}\n Confidence in the answer: {str(round(answer["score"], 3))}')
                # st.text_area(value=context, disabled=True, label="Context", height=500)


if __name__ == "__main__":
    main()
