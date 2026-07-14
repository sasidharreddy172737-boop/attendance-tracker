import streamlit as st
from scraper import attendance

st.set_page_config(page_title="Attendance Tracker", page_icon="📚")
st.title("ATTENDANCE TRACKER")

app = attendance(file="attendance_data.json")

if "selected_sem" not in st.session_state:
    st.session_state.selected_sem = None

if "show_sem_form" not in st.session_state:
    st.session_state.show_sem_form = False

sem_options = ["SEM-1", "SEM-2", "SEM-3", "SEM-4", "SEM-5",
               "SEM-6", "SEM-7", "SEM-8", "+ Add New Semester"]

seme = st.selectbox("SELECT THE SEMESTER:", sem_options)

if st.button("SUBMIT", key="submit_sem"):
    if seme == "+ Add New Semester":
        st.session_state.show_sem_form = True
    else:
        if seme not in app.Sem:
            app.add_sem(seme)
        st.session_state.selected_sem = seme
        st.session_state.show_sem_form = False
        st.success(f"WORKING ON {seme}")

if st.session_state.show_sem_form:
    custom_sem = st.text_input("ENTER YOUR SEM NAME:", key="custom_sem_input")
    if st.button("ADD SEM", key="add_custom_sem"):
        if custom_sem.strip() != "":
            app.add_sem(custom_sem)
            st.session_state.selected_sem = custom_sem
            st.session_state.show_sem_form = False
            st.success(f"ADDED YOUR SEM {custom_sem}")
            st.rerun()
        else:
            st.error("ENTER THE SEM NAME")

if st.session_state.selected_sem:
    st.write(f"WORKING ON: {st.session_state.selected_sem}")

    sem_obj = app.Sem[st.session_state.selected_sem]

    st.subheader(f"ADD THE SUBJECTS TO {st.session_state.selected_sem}")
    new_sub_name = st.text_input("ENTER THE SUBJECT NAME:", key="new_sub_name")
    new_sub_total = st.number_input("ENTER TOTAL NUMBER OF CLASSES:", min_value=1, step=1, key="new_sub_total")

    if st.button("ADD SUBJECT", key="add_subject_btn"):
        if new_sub_name.strip() != "":
            sem_obj.add_subject(new_sub_name, new_sub_total)
            app.save_data()
            st.write(f"{new_sub_name} ADDED")
            st.rerun()
        else:
            st.error("ENTER A SUBJECT NAME")

    st.subheader("YOUR SUBJECTS")
    if len(sem_obj.subj) == 0:
        st.write("NO SUBJECTS")
    else:
        if st.button("MARK ALL"):
            for sub_obj in sem_obj.subj.values():
                sub_obj.mark_attendance("P")
            app.save_data()
            st.success("MARKED ALL")
            st.rerun()

        for sub_name, sub_obj in sem_obj.subj.items():
            with st.container(border=True):
                st.write(f"{sub_name}")
                pct = sub_obj.current_attendance()
                st.write(f"ATTENDANCE:{pct:.1f}%")
                st.write(sub_obj.get_status_message())
                held = sub_obj.present_classes() + sub_obj.absent_classes()
                st.write(f"HELD: {held} | REMAINING: {sub_obj.remaining_classes()}")

                col1, col2, col3, col4 = st.columns(4)

                if col1.button("PRESENT", key=f"present-{sub_name}"):
                    sub_obj.mark_attendance("P")
                    app.save_data()
                    st.rerun()

                if col2.button("ABSENT", key=f"absent-{sub_name}"):
                    sub_obj.mark_attendance("A")
                    app.save_data()
                    st.rerun()

                if col3.button("NO CLASS", key=f"noclass-{sub_name}"):
                    sub_obj.mark_attendance("N")
                    app.save_data()
                    st.rerun()

                if col4.button("DELETE SUBJECT", key=f"delete-{sub_name}"):
                    del sem_obj.subj[sub_name]
                    app.save_data()
                    st.rerun()