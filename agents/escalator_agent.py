import pandas as pd
from typing import Tuple, Optional
from langchain_openai import OpenAI
import re
import os

#Load the escalator prompt template from the markdown file
with open('./prompts/escalator_prompt.md', 'r') as file:
    escalator_prompt_template = file.read()

#Use API key that is securely stored in an environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

#Initialize LangChain's OpenAI LLM with the API key
llm = OpenAI(api_key=OPENAI_API_KEY)

#Load generated emails and lead information
emails_df = pd.read_csv('./data/generated_emails.csv')
leads_df = pd.read_excel('./data/leads.xlsx', engine='openpyxl')

#Merge the data based on 'Name' and 'Job Title'
emails_df = emails_df.rename(columns={"Lead Name": "Name"})
merged_df = pd.merge(leads_df, emails_df, on=["Name", "Job Title"], how="left")

def analyze_and_respond(lead_info: dict) -> Tuple[str, Optional[str]]:
    """
    Parameters:
    - lead_info (dict): A dictionary containing information about the lead and their response
    Returns:
    Tuple[str, Optional[str]]: A tuple where the first element is the lead status ('escalate' or 'ask for details') and the second element is the agent's response or NULL if escalation is advised.
    """
    #Convert lead response to lowercase and search for numbers (indicating budget)
    lead_response = lead_info.get('Lead Response', '').lower()
    numeric_match = re.search(r'\d+', lead_response)
    
    #Check if both 'budget' and 'scope' are mentioned in the lead response
    if 'budget' in lead_response and 'scope' in lead_response:
        if numeric_match:
            #If budget details are mentioned, escalate the lead
            return 'escalate', None
        else:
            #If budget is mentioned without details, ask for more specifics
            details_request_prompt = f"Dear {lead_info.get('Name')},\nThank you for your interest in Antematter. We are interested in '{lead_info.get('Project Title', '')}' but need more details to provide an accurate estimate. Could you specify your budget range and any specific project requirements or goals?"
            return 'ask for details', details_request_prompt
    elif 'more information' in lead_response:
        #If the lead is asking for more information, escalate the lead
        return 'escalate', None
    else:
        #Format the escalator prompt with lead information for other cases
        formatted_prompt = escalator_prompt_template.format(**lead_info)
        response = llm.generate(prompts=[formatted_prompt], max_tokens=200)
    
        if response.flatten() and response.flatten()[0].generations:
            generated_text = response.flatten()[0].generations[0][0].text.strip()
            #Replace placeholder with company name in the generated text
            generated_text = generated_text.replace("[Your Name]", "Antematter.io")
        else:
            #Fallback prompt asking for more project details
            fallback_prompt = f"Your project '{lead_info.get('Project Title', '')}' is intriguing, and we're keen to know more. Could you share further details about the project's scope and any budget considerations to help us tailor our proposal?"
            generated_text = fallback_prompt
        return 'ask for details', generated_text



def process_leads(df: pd.DataFrame) -> pd.DataFrame:
    #Add columns for lead status and agent response
    df['Lead Status'] = ''
    df['Agent Response'] = ''

    for index, row in df.iterrows():
        #Pass the whole lead information as a dictionary
        lead_status, agent_response = analyze_and_respond(row.to_dict())
        df.at[index, 'Lead Status'] = lead_status
        df.at[index, 'Agent Response'] = agent_response if agent_response else "NULL"

    return df

#Process the merged leads and emails
processed_leads_df = process_leads(merged_df)

#Save the processed information
processed_leads_df.to_csv('./data/escalated_leads.csv', index=False)
