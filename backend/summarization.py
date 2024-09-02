import google.generativeai as genai


def summarization(text):
  genai.configure(api_key = "Enter-Your-API_KEY")

  model=genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="Your are an intelligent agent your job is strictly follow the instructions given and perform operations")

  summary = model.generate_content(f"summarize the meeting as big paragraph without missing immportant features from the given text input:{text}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1,
    ))

  plan = model.generate_content(f"Just provide five concise plan of action items presented as bullet points from the text nothing else no heading: {text}",
        generation_config = genai.GenerationConfig(
        temperature=0.1,
    ))

  return summary.text, plan.text