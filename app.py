# 7. RUN EVALUATION
if st.button("🚀 RUN EVALUATION"):
    if not sch_choice or not lesson_input:
        st.warning("Please select a school and paste your lesson plan first!")
    else:
        with st.spinner("Analyzing pedagogical ROI..."):
            p = f"Evaluate this {subject} lesson for {grade} at {sch_choice}. "
            p += f"Class Size: {c_size}, Gender: {g_ratio}% Female. "
            p += f"Needs: {sped_val}% SPED, {fof_val}% 504, {el_val}% EL learners. "
            p += f"Plan: {lesson_input}. "
            p += "Feedback: 1. Cal Poly Professor, 2. Veteran Teacher (ROI), 3. Students."
            
            success = False
            # UPDATED FOR MARCH 9, 2026: Using the newest Gemini 3.1 and 2.5 stable models
            # We are avoiding the '-exp' and '-preview' models that are shutting down today.
            for model_name in ["gemini-3.1-flash", "gemini-2.5-flash", "gemini-2.0-flash-001"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=p
                    )
                    st.session_state["result"] = response.text
                    success = True
                    break
                except Exception as e:
                    # Log the specific error for debugging if needed
                    last_error = str(e)
                    continue
            
            if success:
                st.rerun()
            else:
                st.error(f"March 9th Sync Error: {last_error}. Try again in a few minutes or check Google AI Studio for new model names.")
