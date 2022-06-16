import io

import streamlit as st
from annotated_text import annotation

import doc_file_worker
import model as md
import pdf_extractor as pdfe


def _hide_streamlit_menu():
    hide_menu_style = """
        <style>
        #MainMenu {visibility : hidden; }
        footer {visibility : hidden; }
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def AI_thinking(question: str, option: str):
    with st.spinner("ИИ думает..."):
        return md.get_answer(option, question)


def main():
    st.set_page_config(page_title="Law Finder")
    _hide_streamlit_menu()

    st.title("Law Finder - найдет все ответы.")

    option = st.selectbox(
        'Выберите законодательный акт или добавьте свой документ: ',
        doc_file_worker.get_doc_files())

    if option == "Собственный текст":
        form = st.form(key="FORM")
        with form:
            doc_name = st.text_input("Введите название документа")
            uploaded_file = st.file_uploader(label="Загрузите сюда файл в вашим текстом", type=['txt', 'pdf'])
            submitted = st.form_submit_button(label="Загрузить файл")

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
            question = st.text_area("Вопрос:")
            submitted = st.form_submit_button(label="Получить ответ")
        if submitted:
            print(question, option)
            if question == "":
                st.error("Введите вопрос!")
            if question != "":
                answer, context = AI_thinking(question, option)
                answer_str: str = answer['answer']
                st.write("## Ответ: ")
                st.write("# " + answer_str.strip())
                st.write(f'Уверенность: {str(round(answer["score"], 3))}')

                start_idx = context.find(answer_str)
                end_idx = start_idx + len(answer_str)

                st.write("## Контекст: ")
                st.write(
                    context[:start_idx] + str(annotation(answer_str, "ANSWER", "#8ef")) + context[end_idx:],
                    unsafe_allow_html=True)


if __name__ == "__main__":
    main()
