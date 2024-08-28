import streamlit as st
import json
from send_email import send_mail
from mail_format import process_meeting_details

# File path to store emails
emails_file = r"C:\Users\HP\PycharmProjects\pythonProject\API\mail_cred.json"

# Function to load existing emails from file
def load_emails():
    try:
        with open(emails_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save updated emails to file
def save_emails(emails):
    with open(emails_file, "w") as f:
        json.dump(emails, f)

def send_mail_page():
    # Load existing emails from file
    emails = load_emails()

    changes_made = False

    # Streamlit app layout
    st.title("Meeting Email Management")

    # Option to select meeting types
    selected_meeting_types = st.multiselect("Select Meeting Types to Send Email:", list(emails.keys()))

    # Display selected meeting types and their emails
    st.subheader("Selected Meeting Types and Emails to Send:")
    emails_to_send = []

    for meeting_type in selected_meeting_types:
        st.subheader(f"{meeting_type}:")
        for email in emails.get(meeting_type, []):
            st.text(email)
            emails_to_send.append(email)

    # Retrieve the summary from Streamlit session state
    varrr = """
**Type of meeting:** Team meeting
**Emotion or tone:** Confused, collaborative
**Specific industry or topic:** Technology
**Any particular focus:** Recording and storing meeting data
**Summary:** The team discusses the process of recording and storing meeting data using tools like Microsoft Teams and Zoom. They explore options such as downloading recordings locally or storing them in the cloud. They also consider using the Microsoft Graph API for managing meeting data.
**Plan of Action:**
1. Clarify the process of recording and storing meeting data with the team to ensure everyone understands the options available.
2. Investigate the use of Microsoft Graph API for managing meeting recordings and explore how it can streamline the process.
3. Test different methods of recording and storing meeting data, such as using Microsoft Teams, Zoom, or other tools, to determine the most efficient solution.
4. Create guidelines or documentation on the best practices for recording and storing meeting data to ensure consistency within the team.
5. Consider setting up a dedicated team or group within Microsoft Teams to manage and share meeting recordings effectively.
"""
    summ = st.session_state.get('summary', None)
    if summ:
        st.subheader("Summary and Plan of Action:")
        st.write(summ)

    # Option to send email to selected meeting types
    if st.button("Send Email"):
        if selected_meeting_types:
            emails_to_send = []
            for meeting_type in selected_meeting_types:
                for email in emails.get(meeting_type, []):
                    emails_to_send.append(email)
            if emails_to_send:
                processed_output = process_meeting_details(summ)

                subject = processed_output['particular_focus']
                body = f"""
Dear Team,<br><br>

I hope this email finds you well. The purpose of this message is to highlight the key points discussed in today's meeting:<br><br>

<b>Summary:</b><br>
{processed_output['summary']}<br><br>

<b>Plan of Action:</b><br>
<ul>
{''.join([f'<li>{action}</li>' for action in processed_output['plan_of_action']])}
</ul><br>

<b>Emotion/Tone:</b> {processed_output['emotion_tone']}<br>
<b>Specific Industry/Topic:</b> {processed_output['specific_industry_topic']}<br><br>

Your prompt attention to these matters is appreciated.<br><br>

Best regards,<br>
Nihal Thomas
"""
                send_mail(emails_to_send, subject, body)
                st.success(f"Email sent to: {', '.join(emails_to_send)}")
            else:
                st.warning("No emails selected to send.")
        else:
            st.warning("Please select at least one meeting type.")

    # Option to add new email for any meeting type
    st.subheader("Add New Email:")
    new_email = st.text_input("Add new email:")
    meeting_types_for_new_email = st.multiselect("Select Meeting Types to Add Email:", list(emails.keys()))

    # Button to add new email

    if st.button("Add New Email"):
        if new_email and meeting_types_for_new_email:
            for meeting_type in meeting_types_for_new_email:
                if meeting_type in emails:
                    if new_email not in emails[meeting_type]:
                        emails[meeting_type].append(new_email)
                        changes_made = True
                else:
                    emails[meeting_type] = [new_email]
                    changes_made = True
            # Save updated emails to file if changes were made
            if changes_made:
                save_emails(emails)
                st.success(f"New email '{new_email}' added to selected meeting types.")
            else:
                st.warning("No changes were made.")
        elif not new_email:
            st.warning("Please enter an email to add.")
        elif not meeting_types_for_new_email:
            st.warning("Please select at least one meeting type to add the email to.")

    # Remove email section
    st.subheader("Remove Email:")

    # Option to select meeting type to remove emails from
    selected_meeting_type = st.selectbox("Select Meeting Type to Remove Emails From:", list(emails.keys()))

    if selected_meeting_type:
        st.subheader(f"Emails for {selected_meeting_type}:")
        emails_to_remove = st.multiselect("Select Emails to Remove:", emails[selected_meeting_type])

        if st.button("Remove"):
            if emails_to_remove:
                # Remove selected emails from the list
                emails[selected_meeting_type] = [email for email in emails[selected_meeting_type] if email not in emails_to_remove]
                changes_made = True  # Ensure changes are detected
                st.success("Selected emails removed successfully.")
                # Save updated emails to file after removal
                save_emails(emails)
            else:
                st.warning("No emails selected to remove.")
