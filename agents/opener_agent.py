import pandas as pd
import os
from langchain.llms import OpenAI as LangChainOpenAI

#constants for default sender information
DEFAULT_SENDER_NAME = "xyz"  #sender's name for email signature
DEFAULT_SENDER_EMAIL = "contact@xyz.inc"  #sender's email for email signature
DEFAULT_COMPANY_NAME = "xyz.inc"  

# Load the email prompt template from markdown file
with open('./prompts/email_prompt.md', 'r') as file:
    email_prompt_template = file.read()

def generate_email(lead_info: dict, max_tokens=300, temperature=0.7) -> dict:
    """
    Generates personalized emails for each lead using the provided template and lead information.

    :param lead_info: A dictionary containing the lead's information
    :param max_tokens: Max number of tokens for the generated email
    :param temperature: Controls the randomness of the output
    :return: A dictionary with email details including model name, temperature, lead details, email subject, and email body.
    """
    #format the prompt with specific lead information
    prompt = email_prompt_template.format(
        name=lead_info['Name'],
        job_title=lead_info['Job Title'],
        organization=lead_info['Organizaton'], 
        project_title=lead_info['Project Title'],
        looking_for=lead_info['Looking For']
    )

    #using the OpenAI API key stored in an environment variable for security
    openai_api_key = os.getenv('OPENAI_API_KEY')
    llm = LangChainOpenAI(api_key=openai_api_key)

    #generate email content using the formatted prompt
    response = llm.generate([prompt], max_tokens=max_tokens, temperature=temperature)

    #flatten the response to extract the generated text
    flat_results = response.flatten()
    generated_text = flat_results[0].generations[0][0].text.strip() if flat_results and flat_results[0].generations else "No response generated."

    #Assuming the first line is the subject if it starts with 'Subject:', else use a default subject
    email_subject, email_body = ("Software Consultancy Inquiry", generated_text) if not generated_text.startswith('Subject:') else generated_text.split('\n\n', 1)
    email_subject = email_subject.replace('Subject:', '').strip()
    
    #ensure the email body contains at maximum three paragraphs. also add the sender's signature
    email_body = "\n\n".join(email_body.split('\n\n')[:3]) + f"\n\nBest regards,\n{DEFAULT_SENDER_NAME}\n{DEFAULT_SENDER_EMAIL}"

    #Return email details
    return {
        "Model Name": response.llm_output.get('model_name', 'Unknown'),
        "Temperature": temperature,
        "Lead Name": lead_info['Name'],
        "Job Title": lead_info['Job Title'],
        "Prompt": prompt,
        "Email Subject": email_subject,
        "Email Body": email_body.strip()
    }

#Load leads information from an excel file (this leads file has been formatted using code to remove empty rows and columns)
leads_df = pd.read_excel('./data/leads.xlsx', engine='openpyxl')

#Generate personalized emails for each lead
results = [generate_email(lead_info.to_dict()) for _, lead_info in leads_df.iterrows()]

#Save the generated emails to a CSV file
emails_df = pd.DataFrame(results)
emails_df.to_csv('./data/generated_emails.csv', index=False)
