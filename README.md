# Antematter Sales Assistance Solution

This solution automates the management and response process to leads for Antematter's sales department, encompassing two pivotal components: the Opener Agent and the Escalator Agent.

## Overview

- **Opener Agent**: Crafts personalized emails to initiate conversations with leads, aiming to gather more information on their project scope and budget.
- **Escalator Agent**: Analyzes leads' responses to determine the next steps, such as escalating the conversation or requesting further details.

## Prerequisites

- Python 3.12.2

## Installation

1. Clone this repository to your local machine to get started.
2. Install the necessary dependencies by running the following command in your terminal:

pip install -r requirements.txt


## Usage

- **Generating Opening Emails (Opener Agent)**:
Execute the Opener Agent script to generate opening emails for each lead:

python opener_agent.py

- **Escalator Agent**:
Process lead responses with:

python escalator_agent.py


## Input Data

Lead information is provided in an Excel file `leads.xlsx`, with responses to be processed by the Escalator Agent.

## Output

- The Opener Agent generates `generated_emails.csv` containing email subjects and bodies.
- The Escalator Agent outputs `escalated_leads.csv`, indicating if a lead was escalated or more details are required, along with any generated responses.

## Project Structure

.

├── agents/

│ ├── opener_agent.py # Script for the Opener Agent

│ └── escalator_agent.py # Script for the Escalator Agent

├── prompts/

│ ├── email_prompt.md # Markdown file with the email prompt for the Opener Agent

│ └── escalator_prompt.md # Markdown file with the response prompt for the Escalator Agent

├── data/
│ ├── leads.xlsx # Excel file with lead information

│ ├── generated_emails.csv # CSV output from the Opener Agent

│ └── escalated_leads.csv # CSV output from the Escalator Agent

├── README.md 

└── requirements.txt 


## License

This project is licensed under the MIT License.

## Contact

For queries or more information, contact areebaayaz76@gmail.com.
