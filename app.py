"""
CliftonStrengths Comparison App - Streamlit Application
"""

import streamlit as st
from strengths import CLIFTON_STRENGTHS, validate_strengths, format_strengths_list
from openai_service import compare_strengths
from data_storage import load_saved_people, save_person, delete_person, get_person_strengths


def check_password():
    """
    Returns `True` if the user has entered the correct password.
    """
    
    def get_password():
        """Get password from secrets or use default."""
        try:
            if hasattr(st, 'secrets') and "app_password" in st.secrets:
                return st.secrets["app_password"]
        except:
            pass
        # Default password for local development
        return "strengths2024"
    
    def password_entered():
        """Check if the entered password is correct."""
        if st.session_state["password_input"] == get_password():
            st.session_state["password_correct"] = True
            # Don't store the actual password
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False
    
    # Check if password has been validated
    if st.session_state.get("password_correct", False):
        return True
    
    # Show password input
    st.markdown("### 🔒 CliftonStrengths Comparison Tool")
    st.markdown("This app is password protected. Please enter the password to continue.")
    
    st.text_input(
        "Password",
        type="password",
        on_change=password_entered,
        key="password_input",
        placeholder="Enter password..."
    )
    
    # Show error if password was wrong
    if st.session_state.get("password_correct", None) == False:
        st.error("😕 Incorrect password. Please try again.")
    
    st.info("💡 **Tip:** Contact the app owner if you need access.")
    
    return False


def render_person_selector(person_number, is_me=False):
    """
    Render the person selection and strengths input section.
    
    Args:
        person_number (int): 1 or 2
        is_me (bool): Whether this is the "Me" person
        
    Returns:
        tuple: (name, strengths_list)
    """
    # Load saved people
    saved_people = load_saved_people()
    saved_names = list(saved_people.keys())
    
    # Header
    header = f"👤 Person {person_number}"
    if is_me:
        header += " (Me)"
    st.subheader(header)
    
    # Handle pending selection changes (set before widget creation)
    pending_key = f"person{person_number}_pending_selection"
    selection_key = f"person{person_number}_selection"
    last_selection_key = f"person{person_number}_last_selection"
    
    if pending_key in st.session_state:
        st.session_state[selection_key] = st.session_state[pending_key]
        del st.session_state[pending_key]
    
    # Initialize selection if not exists
    if selection_key not in st.session_state:
        st.session_state[selection_key] = "➕ Add New Person"
    
    # Dropdown to select saved person or add new
    options = ["➕ Add New Person"] + saved_names
    
    # Validate that current selection is still valid
    if st.session_state[selection_key] not in options:
        st.session_state[selection_key] = "➕ Add New Person"
    
    selected = st.selectbox(
        "Select a person",
        options=options,
        key=selection_key
    )
    
    # Check if selection changed - if so, clear the strength session state
    if last_selection_key in st.session_state:
        if st.session_state[last_selection_key] != selected:
            # Selection changed - clear strength values
            for i in range(5):
                strength_key = f"person{person_number}_strength_{i}"
                if strength_key in st.session_state:
                    del st.session_state[strength_key]
    
    # Update last selection
    st.session_state[last_selection_key] = selected
    
    # Initialize variables
    person_name = ""
    person_strengths = []
    
    # If selecting saved person, load their data
    if selected != "➕ Add New Person":
        person_name = selected
        saved_strengths = get_person_strengths(selected)
        if saved_strengths:
            person_strengths = saved_strengths
        
        # Show name (read-only)
        st.text_input(
            "Name",
            value=person_name,
            key=f"person{person_number}_name_display",
            disabled=True
        )
    else:
        # Input for new person
        person_name = st.text_input(
            "Name",
            placeholder="Enter name...",
            key=f"person{person_number}_name_input"
        )
    
    # Strengths selection
    st.markdown("**Top 5 CliftonStrengths:**")
    
    # Initialize session state for strengths if needed
    for i in range(5):
        strength_key = f"person{person_number}_strength_{i}"
        if strength_key not in st.session_state and person_strengths and i < len(person_strengths):
            st.session_state[strength_key] = person_strengths[i]
    
    current_strengths = []
    for i in range(5):
        strength_key = f"person{person_number}_strength_{i}"
        
        # Determine default index
        default_index = 0
        if person_strengths and i < len(person_strengths):
            try:
                default_index = CLIFTON_STRENGTHS.index(person_strengths[i]) + 1
            except ValueError:
                default_index = 0
        
        strength = st.selectbox(
            f"Strength #{i+1}",
            options=["Select a strength..."] + CLIFTON_STRENGTHS,
            key=strength_key,
            index=default_index if selected != "➕ Add New Person" else 0
        )
        current_strengths.append(strength)
    
    # Save button
    save_col, delete_col = st.columns([1, 1])
    with save_col:
        if st.button(f"💾 Save Person {person_number}", key=f"save_person{person_number}", use_container_width=True):
            # Validate before saving
            valid_strengths = [s for s in current_strengths if s != "Select a strength..."]
            
            if not person_name or not person_name.strip():
                st.error("Please enter a name before saving.")
            elif len(valid_strengths) != 5:
                st.error("Please select all 5 strengths before saving.")
            elif len(valid_strengths) != len(set(valid_strengths)):
                st.error("Please select 5 different strengths (no duplicates).")
            else:
                if save_person(person_name.strip(), valid_strengths):
                    st.success(f"✅ {person_name} saved successfully!")
                    # Use pending key to update selection on next run
                    st.session_state[f"person{person_number}_pending_selection"] = person_name.strip()
                    st.rerun()
                else:
                    st.error("Failed to save person. Please try again.")
    
    with delete_col:
        if selected != "➕ Add New Person":
            if st.button(f"🗑️ Delete", key=f"delete_person{person_number}", use_container_width=True):
                if delete_person(selected):
                    st.success(f"✅ {selected} deleted.")
                    # Use pending key to update selection on next run
                    st.session_state[f"person{person_number}_pending_selection"] = "➕ Add New Person"
                    # Clear strength selections
                    for i in range(5):
                        strength_key = f"person{person_number}_strength_{i}"
                        if strength_key in st.session_state:
                            del st.session_state[strength_key]
                    st.rerun()
                else:
                    st.error("Failed to delete person.")
    
    return person_name, current_strengths


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="CliftonStrengths Comparison",
        page_icon="💪",
        layout="wide"
    )
    
    # Check password first
    if not check_password():
        st.stop()
    
    # Title and description
    st.title("🎯 CliftonStrengths Comparison Tool")
    st.markdown(
        "Compare CliftonStrengths profiles between two people to understand "
        "potential conflicts, collaboration opportunities, and communication strategies."
    )
    st.divider()
    
    # Create two columns for the two people
    col1, col2 = st.columns(2)
    
    # Person 1 inputs (Me)
    with col1:
        person1_name, person1_strengths = render_person_selector(1, is_me=True)
    
    # Person 2 inputs
    with col2:
        person2_name, person2_strengths = render_person_selector(2, is_me=False)
    
    st.divider()
    
    # Compare button
    compare_button = st.button("🔍 Compare Strengths", type="primary", use_container_width=True)
    
    if compare_button:
        # Validation
        errors = []
        
        # Check names
        if not person1_name or not person1_name.strip():
            errors.append("Please enter a name for Person 1.")
        if not person2_name or not person2_name.strip():
            errors.append("Please enter a name for Person 2.")
        
        # Validate Person 1 strengths
        valid1, error1 = validate_strengths(person1_strengths)
        if not valid1:
            errors.append(f"Person 1: {error1}")
        
        # Validate Person 2 strengths
        valid2, error2 = validate_strengths(person2_strengths)
        if not valid2:
            errors.append(f"Person 2: {error2}")
        
        # Display errors if any
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Clean up names
            person1_name = person1_name.strip()
            person2_name = person2_name.strip()
            
            # Filter out placeholder selections
            person1_strengths = [s for s in person1_strengths if s != "Select a strength..."]
            person2_strengths = [s for s in person2_strengths if s != "Select a strength..."]
            
            # Show comparison summary
            st.success(f"Comparing {person1_name} and {person2_name}...")
            
            with st.expander("📊 Strengths Summary", expanded=True):
                sum_col1, sum_col2 = st.columns(2)
                with sum_col1:
                    st.markdown(f"**{person1_name}'s Strengths:**")
                    for strength in person1_strengths:
                        st.markdown(f"- {strength}")
                with sum_col2:
                    st.markdown(f"**{person2_name}'s Strengths:**")
                    for strength in person2_strengths:
                        st.markdown(f"- {strength}")
            
            # Call OpenAI API
            try:
                with st.spinner("🤔 Analyzing strengths profiles with AI..."):
                    conflicts, collaboration, communication = compare_strengths(
                        person1_name,
                        person1_strengths,
                        person2_name,
                        person2_strengths
                    )
                
                # Display results
                st.divider()
                st.header("📋 Analysis Results")
                
                # Question 1: Conflicts
                st.subheader("⚠️ What conflicts might we have?")
                with st.container():
                    st.markdown(conflicts)
                
                st.divider()
                
                # Question 2: Collaboration
                st.subheader("🤝 How can we work well together?")
                with st.container():
                    st.markdown(collaboration)
                
                st.divider()
                
                # Question 3: Communication
                st.subheader(f"💬 How should {person1_name} speak to {person2_name}?")
                with st.container():
                    st.markdown(communication)
                
            except ValueError as e:
                st.error(f"⚙️ Configuration Error: {str(e)}")
                st.info(
                    "💡 **Tip:** Make sure the OPENAI_API_KEY environment variable is set. "
                    "If running with Docker, use: "
                    "`docker run -e OPENAI_API_KEY=your_key_here ...`"
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info(
                    "Please check your internet connection and API key, then try again."
                )
    
    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
        "Powered by OpenAI GPT-4o | CliftonStrengths® is a registered trademark of Gallup, Inc."
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
