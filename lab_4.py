from google.colab import drive
drive.mount('/content/drive')

import os
import shutil
from google.colab import userdata

# --- CONFIGURATION ---
# Make sure this matches the EXACT name of your notebook in Google Drive
NOTEBOOK_NAME = "lab_4.ipynb"
GITHUB_USERNAME = "avatarmongacancode34"
REPO_NAME = "lab-4-llm-decision-support"
USER_EMAIL = "shaun.sibanda@ashesi.edu.gh"
COMMIT_MESSAGE = "reflections left"
# ---------------------

try:
    token = userdata.get('LAB_4')
    repo_url = f"https://{token}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
except userdata.SecretNotFoundError:
    print("ERROR: LAB_4 token not found.")
    token = None

if token:
    # 1. Paths
    drive_path = f"/content/drive/MyDrive/Colab Notebooks/{NOTEBOOK_NAME}"
    repo_path = f"/content/{REPO_NAME}"
    dest_path = f"{repo_path}/{NOTEBOOK_NAME}"

    if not os.path.exists(drive_path):
        print(f"ERROR: Could not find '{NOTEBOOK_NAME}' in your Drive.")
    else:
        # 2. Setup Git & Clone if needed
        os.chdir('/content')
        !git config --global user.email "{USER_EMAIL}"
        !git config --global user.name "{GITHUB_USERNAME}"

        if not os.path.exists(REPO_NAME):
            !git clone {repo_url}
        else:
            os.chdir(REPO_NAME)
            !git pull origin main
            os.chdir('/content')

        # 3. Copy the latest saved version from Drive into the Git repo
        shutil.copy2(drive_path, dest_path)
        print(f"Copied latest version of {NOTEBOOK_NAME} from Drive.")

        # 4. Commit and Push
        os.chdir(repo_path)
        !git add {NOTEBOOK_NAME}
        !git commit -m "{COMMIT_MESSAGE}"
        !git push origin main
        print("Successfully pushed to GitHub!")



# API-key setup — DO NOT hard-code your key in this cell.

import os



# --- Google Colab (Secrets panel) ---
from google.colab import userdata
API_KEY = userdata.get("GROQ")

# TODO: set API_KEY using ONE of the methods above.

# OpenAI-compatible client (works for Groq and OpenAI; Gemini users see their docs):
from openai import OpenAI

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",   # remove this line if using OpenAI itself
)
MODEL = "llama-3.3-70b-versatile"                # or your provider's model name

print("Client ready.")



# TODO: Write a helper function you will reuse for the WHOLE lab:
#
def ask_llm(user_prompt, system_prompt="You are a helpful assistant.",
             temperature=0.7, max_tokens=500):
     response = client.chat.completions.create(model=MODEL,
         messages=[
             {"role": "system", "content": system_prompt},
             {"role": "user",   "content": user_prompt},
         ],
         temperature=temperature,
         max_tokens=max_tokens,
     )
     return response.choices[0].message.content, response.usage

print(ask_llm("What is the capital of France?"))
#
# TODO: Call it once with a simple question and print the answer.
# TODO: Print response.usage as well — how many tokens did your call consume?

# TODO: Ask the SAME question 5 times at temperature=0.0 and 5 times at temperature=1.2.
#   A good test question: "Suggest a name for a savings product for market traders in Accra."

# TODO: Print all 10 answers, grouped by temperature.
print("Tempereture = 0 responses: ")
for i in range(5):
  print(ask_llm("Suggest a name for a savings product for market traders in Accra.", temperature=0.0)[0])
print("------------------------------------------------------------------------------")
print("Tempereture = 1.2 responses: ")
for i in range(5):
  print(ask_llm("Suggest a name for a savings product for market traders in Accra.", temperature=1.2)[0])

LETTERS = {
"L001": """Dear Sir/Madam,
My name is Akosua Mensah and I have been selling provisions at Makola Market for 12 years.
I am applying for a loan of GHS 8,000 to buy a deep freezer and expand into frozen foods.
My current stall makes about GHS 900 profit each month. I have saved GHS 2,500 with your
susu scheme over the past two years and I have never missed a contribution. I can repay
GHS 450 monthly over 20 months. My sister, a teacher, will stand as my guarantor.
Thank you for considering my application.""",

"L002": """Hello,
I am Kwame Boateng, a commercial driver in Kumasi. I need GHS 25,000 urgently to repair my
trotro engine and settle some personal debts. Business has been slow but it will surely
pick up after the festive season. I can pay back whenever the money comes. I do not have
collateral at the moment but God willing everything will be fine. Please help me quickly.""",

"L003": """Dear Loan Committee,
I am Efua Darko, owner of Darko Fashions, a registered dressmaking business in Takoradi
(registration no. BN-2019-4482). I employ three apprentices. I request GHS 15,000 to
purchase two industrial sewing machines and fabric stock ahead of the Christmas season.
Last year my December revenue alone was GHS 22,000; monthly profit averages GHS 2,800.
I hold a fixed deposit of GHS 5,000 with GCB which I can pledge. Proposed repayment:
GHS 1,100 monthly for 15 months. Attached are my sales records for the past 18 months.""",

"L004": """Good day,
My name is Yaw Owusu. I want a loan for my poultry farm at Nsawam. The amount is GHS 12,000
for feed and 500 new layers. I started the farm last year. Sometimes I make good money,
around GHS 1,500 in a good month, but bird flu affected us in March and I lost many birds.
I am rebuilding now. I can repay in 18 months. My uncle has agreed to guarantee the loan
with his taxi.""",

"L005": """Dear Manager,
I am writing on behalf of the Adenta Women's Weaving Cooperative (14 members). We seek
GHS 30,000 to buy a bulk order of yarn directly from the factory, cutting out middlemen and
raising our margins from 15% to about 35%. The cooperative has operated for 6 years and
holds GHS 9,000 in our group account. We propose repayment of GHS 2,000 monthly over
16 months, backed by our group savings and joint liability agreement.""",

"L006": """Hi,
This is Kofi. I saw your advert. I want GHS 50,000 to start a car washing business, a
provision shop, and also import phones from Dubai. I am 22 and full of energy. I have not
started any of these yet but my friends say I am very business minded. I will pay back in
one year when the businesses are booming. No collateral but I am trustworthy.""",
}

# Gold-standard labels for three letters (for Section 4 evaluation):
GOLD = {
  "L001": {"applicant_name": "Akosua Mensah", "amount_ghs": 8000,  "purpose": "buy deep freezer / expand into frozen foods",
           "monthly_profit_ghs": 900,  "has_collateral_or_guarantor": True,  "repayment_months": 20},
  "L003": {"applicant_name": "Efua Darko",    "amount_ghs": 15000, "purpose": "industrial sewing machines and fabric stock",
           "monthly_profit_ghs": 2800, "has_collateral_or_guarantor": True,  "repayment_months": 15},
  "L006": {"applicant_name": "Kofi",          "amount_ghs": 50000, "purpose": "car wash, provision shop, phone imports",
           "monthly_profit_ghs": None, "has_collateral_or_guarantor": False, "repayment_months": 12},
}

print(f"{len(LETTERS)} letters loaded.")

# TODO: Write SUMMARY_PROMPT_V1 — your first, naive attempt (e.g. just "Summarize this:").
#   Run it on L002 and L006. Read the output critically.

print("version 1: ")

SUMMARY_PROMPT_V1 = "Summarize this: "
print(ask_llm(SUMMARY_PROMPT_V1 + LETTERS["L002"], temperature = 0)[0])
print(ask_llm(SUMMARY_PROMPT_V1 + LETTERS["L006"],temperature=0)[0])

print("------------------------------------------------------------------------------")
print("version 2")

SUMMARY_PROMPT_V2 = """You are an assistant to a microfinance loan officer.
Your task is to summarize loan applications.

Constraints:
1. Be factual and neutral.
2. Do not invent, or hallucinate any details.
3. The summary must be exactly 3 to 4 sentences long.
4. Focus strictly on: applicant background, requested loan amount, purpose, income/business details, and collateral offered.
"""
print(ask_llm(SUMMARY_PROMPT_V2 + LETTERS["L002"],temperature=0)[0])
print(ask_llm(SUMMARY_PROMPT_V2 + LETTERS["L006"],temperature=0)[0])
# TODO: Now write SUMMARY_PROMPT_V2 as a proper template with:
#   - a system prompt giving the LLM a ROLE (e.g. "You are an assistant to a microfinance
#     loan officer...") and constraints (factual, neutral, no invented details, 3-4 sentences)
#   - a user prompt template like: f"Summarize this loan application:\n\n{letter_text}"
#   Run V2 on the same two letters at temperature=0.

# TODO: Compare V1 vs V2 outputs side by side. Keep both prompt versions in this notebook.

# TODO: Write EXTRACT_PROMPT — a template that instructs the model to return ONLY a JSON
#   object with EXACTLY these keys:
#     applicant_name (string), amount_ghs (number), purpose (string),
#     monthly_profit_ghs (number or null), has_collateral_or_guarantor (boolean),
#     repayment_months (number or null)
#   Techniques to use:
#     - explicit schema in the prompt
#     - ONE worked example (few-shot) using a letter you write yourself (not from LETTERS!)
#     - "If a field is not stated in the letter, use null. Do not guess."
#     - temperature=0
EXTRACT_PROMPT = """You are a data extraction system for microfinance loans.
Your only output must be a JSON object. Do not include introductory text, explanations, or markdown formatting blocks.
return in the following formart
{
    "applicant_name": "string",
    "amount_ghs": "number (convert any other currencies to numbers if possible, otherwise null)",
    "purpose": "string",
    "monthly_profit_ghs": "number or null",
    "has_collateral_or_guarantor": "boolean",
    "repayment_months": "number or null"
} If a field is not explicitly stated or calculable from the letter, use null. Do NOT guess.

EXAMPLE

Letter:
My name is Thabani. I run a shoe repair stall. I need a loan of 500 GHS to buy new leather and glue. I make about 150 GHS a month in profit. My uncle has agreed to sign as my guarantor. I hope to pay it back over 4 months.

JSON Output:
{
    "applicant_name": "Thabani",
    "amount_ghs": 500,
    "purpose": "buy new leather and glue",
    "monthly_profit_ghs": 150,
    "has_collateral_or_guarantor": true,
    "repayment_months": 4
}


Extract data from this loan application:

[letter_text]
"""


# TODO: Write extract_fields(letter_text) that calls the LLM, strips any ```json fences,
#   json.loads() the result, and returns a dict. Handle parse failures gracefully
#   (return None and print a warning).
import json

def extract_fields(letter_tex, temp = 0.0):
    prompt = EXTRACT_PROMPT.replace("[letter_text]",letter_text)

    try:
        raw_response = ask_llm(
            user_prompt=prompt,
            temperature=temp
        )[0]


        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        cleaned_response = cleaned_response.strip()


        return json.loads(cleaned_response)

    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse JSON.\nError: {e}\nRaw Output:\n{raw_response}")
        return None
    except Exception as e:
        print(f"Warning: API call error: {e}")
        return None

# TODO: Run it on ALL SIX letters; collect results into a pandas DataFrame (one row per
#   letter) and display it.

import pandas as pd
from IPython.display import display


extracted_data_list = []



# Loop through each letter in dataset
for letter_id, letter_text in LETTERS.items():


    #extraction function
    extracted_dict = extract_fields(letter_text)

    if extracted_dict is not None:

        extracted_dict["letter_id"] = letter_id
        extracted_data_list.append(extracted_dict)
    else:
        print(f"Failed to extract structured data for {letter_id}")
        extracted_data_list.append({"letter_id": letter_id})


df = pd.DataFrame(extracted_data_list)


cols = ['letter_id'] + [col for col in df.columns if col != 'letter_id']
df = df[cols]
display(df)


# TODO: Write BRIEF_PROMPT — it receives the letter AND your extracted JSON, and must output:
#     1. Strengths (bullet points, grounded in the letter)
#     2. Risks / red flags (bullet points)
#     3. Missing information the officer should request
#     4. Suggested next step (e.g. "invite for interview", "request documents",
#        "flag for senior review") — NOT "approve" or "reject".
#   Give the model an explicit instruction that final decisions are made by humans.
BRIEF_PROMPT = """You are an AI decision support assistant for a microfinance loan officer.
Your role is to analyze a loan application and provide a brief to assist the human officer.
You do NOT have the authority to approve or reject a loan. Final decisions are strictly made by human officers. Your job is to surface insights and recommend a process-oriented next step.
Analyze the following application using the raw letter and the pre-extracted JSON data.
[RAW LETTER]
[LETTER_TEXT]

[EXTRACTED DATA]
[JSON_DATA]

Output your analysis  in the following format:

### 1. Strengths
* (List bullet points grounded only in the provided text)

### 2. Risks / Red Flags
* (List bullet points highlighting potential issues, inconsistencies, or risks)

### 3. Missing Information
* (List specific documents, figures, or details the officer needs to request)

### 4. Suggested Next Step
(Provide exactly one process recommendation, such as "Invite for interview", "Request guarantor documents", "Flag for senior review", or "Conduct site visit". Do NOT recommend "Approve" or "Reject".)
"""

# TODO: Generate briefs for ALL SIX letters. Print the briefs for L001, L002, and L006 —
#   three very different applications.
decision_briefs = {}

print("Generating decision-support briefs\n")

for letter_id, letter_text in LETTERS.items():

    row_data = df[df['letter_id'] == letter_id].drop(columns=['letter_id'])
    json_string = row_data.to_json(orient='records', lines=True)

    # the prompt
    prompt = BRIEF_PROMPT.replace("[LETTER_TEXT]", letter_text)
    prompt = prompt.replace("[JSON_DATA]", json_string)

    #prompting the ai
    raw_response = ask_llm(
        user_prompt=prompt,
    )[0]

    decision_briefs[letter_id] = raw_response
print(decision_briefs["L001"])
print("------------------------------------------------------------------------------")
print(decision_briefs["L002"])
print("------------------------------------------------------------------------------")
print(decision_briefs["L006"])

import os
repo_dir = f"/content/lab-4-llm-decision-support"
if os.path.exists(repo_dir):
    os.chdir(repo_dir)

prompts_code = f"""
SUMMARY_PROMPT = '{SUMMARY_PROMPT_V2}'
EXTRACT_PROMPT = '{EXTRACT_PROMPT}'
BRIEF_PROMPT = '{BRIEF_PROMPT}'
"""
with open("prompts.py", "w") as f:
    f.write(prompts_code)
!git add prompts.py
!git commit -m "added prompts"
!git push origin main
!git rev-parse HEAD


# TODO: For the three letters in GOLD, compare your extracted DataFrame to the gold values
#   field by field. Compute per-field accuracy across the three letters
#   (name matching can be case-insensitive; numbers must match exactly).

# TODO: Display a small table: rows = fields, columns = L001 / L003 / L006 / accuracy.

fields = [
    "applicant_name",
    "amount_ghs",
    "purpose",
    "monthly_profit_ghs",
    "has_collateral_or_guarantor",
    "repayment_months"
]

target_letters = ["L001", "L003", "L006"]
evaluation_results = []

def safe_compare(pred, gold, field_name):
    # Handle Nulls/Missing values
    if pd.isna(pred) and pd.isna(gold):
        return True
    if pd.isna(pred) or pd.isna(gold):
        return False

    if field_name in ["applicant_name", "purpose"] and isinstance(pred, str) and isinstance(gold, str):
        return pred.lower().strip() == gold.lower().strip()


    return pred == gold


for field in fields:
    row_result = {"Field": field}
    correct_count = 0

    for letter_id in target_letters:
        pred_row = df[df['letter_id'] == letter_id]
        pred_val = pred_row.iloc[0][field]
        gold_val = GOLD[letter_id].get(field)
        is_match = safe_compare(pred_val, gold_val, field)
        row_result[letter_id] = "Match" if is_match else f" wrong {pred_val} (Gold: {gold_val})"
        if is_match:
            correct_count += 1

    accuracy_percent = (correct_count / len(target_letters)) * 100
    row_result["Accuracy"] = f"{accuracy_percent:.0f}%"
    evaluation_results.append(row_result)


eval_df = pd.DataFrame(evaluation_results)
eval_df.set_index("Field", inplace=True)


display(eval_df)

# TODO: Run extract_fields() on letter L004 FIVE times at temperature=0 and FIVE times at
#   temperature=1.0.

# TODO: For each temperature, report how many of the 5 runs produced (a) valid JSON and
#   (b) identical values across runs. A simple approach: json.dumps(result, sort_keys=True)
#   and count unique strings.

letter_l004 = LETTERS["L004"]
temperatures_to_test = [0.0, 1.0]

for temp in temperatures_to_test:
    valid_count = 0
    stringified_results = []

    for i in range(5):
        result = extract_fields(letter_l004, temp)

        if result is not None:
            valid_count += 1
            result_str = json.dumps(result, sort_keys=True)
            stringified_results.append(result_str)

    unique_variations = len(set(stringified_results))

    print(f"Valid JSON Outputs: {valid_count}/5")
    if valid_count > 0:
        print(f"Unique Data Variations: {unique_variations} (1 means perfectly consistent)\n")
    else:
        print(f"Unique Data Variations: N/A (No valid JSON produced)\n")


# TODO: Design TWO adversarial tests and run them:
#   Test 1 — Ask your summarizer a question about a detail that is NOT in a letter
#     (e.g. "What is the applicant's credit score?"). Does it admit the information is
#     absent, or does it invent one?
#   Test 2 — Feed your extractor an EMPTY or IRRELEVANT text (e.g. a weather report).
#     Does it return nulls, or does it fabricate an applicant?

# TODO: Record the outputs verbatim below and label each PASS or FAIL.
import json
target_letter = LETTERS["L001"]
test_1_prompt = f"What is the applicant's credit score? Answer based ONLY on this application:\n\n{target_letter}"

test_1_output = ask_llm(
    user_prompt=test_1_prompt,

    temperature=0.0
)
print("Query: What is the applicant's credit score?")
print("Output:\n", test_1_output)
print("------------------------------------------------------------------------------")
weather_report = "The weather in Accra today is 32 degrees Celsius with scattered thunderstorms. High humidity is expected."
test_2_output = extract_fields(weather_report)

print("Query: [Weather Report]")
print("Output:")

print(json.dumps(test_2_output, indent=2))

