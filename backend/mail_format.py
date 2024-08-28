def process_meeting_details(text):
    # Split the input text into lines
    lines = text.strip().split('\n')

    # Extract different parts of the output
    meeting_type = ""
    emotion_tone = ""
    specific_industry_topic = ""
    particular_focus = ""
    summary = ""
    plan_of_action = []

    for line in lines:
        if line.startswith("**Type of meeting:**"):
            meeting_type = line.split("**Type of meeting:** ")[1].strip()
        elif line.startswith("**Emotion or tone:**"):
            emotion_tone = line.split("**Emotion or tone:** ")[1].strip()
        elif line.startswith("**Specific industry or topic:**"):
            specific_industry_topic = line.split("**Specific industry or topic:** ")[1].strip()
        elif line.startswith("**Any particular focus:**"):
            particular_focus = line.split("**Any particular focus:** ")[1].strip()
        elif line.startswith("**Summary:**"):
            summary = line.split("**Summary:** ")[1].strip()
        elif line.startswith("**Plan of Action:**"):
            plan_start_index = lines.index(line) + 1
            plan_of_action = [line.strip() for line in lines[plan_start_index:]]
            break

    return {
        "meeting_type": meeting_type,
        "emotion_tone": emotion_tone,
        "specific_industry_topic": specific_industry_topic,
        "particular_focus": particular_focus,
        "summary": summary,
        "plan_of_action": plan_of_action
    }