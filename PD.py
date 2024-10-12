import os
import google.generativeai as genai
import textwrap

path = r"C:\Users\leleq\Code Sprint\Data" ## Change accordingly##

#Set the API_KEY environment variable
#API key from gemini account
os.environ["API_KEY"] = "AIzaSyCiElgnWd-dN78SKIit8h6E0gj9hl7U6GQ"

genai.configure(api_key=os.environ["API_KEY"])

#configurations for AI output - variables
generation_config = {
"temperature": 0,
"top_p": 1,
"top_k": 1
}

model = genai.GenerativeModel("gemini-1.5-flash") ## different model to upload files##

prompt_1 = "Access the suitability of this candidate for this project. Give a rating out of 10, and explain why. \n\n"
prompt_2 = "Rank the following candidates in terms of their suitability to the project, indicate who is not suitable, and nominate a leader out of them. \n\n"

for PD_file_name in os.listdir(rf"{path}\PD"):
    PD_pdf = genai.upload_file(rf"{path}\PD\{PD_file_name}")
    for YER_file_name in os.listdir(rf"{path}\YER"):
        YER_pdf = genai.upload_file(rf"{path}\YER\{YER_file_name}")
        response = model.generate_content([prompt_1, YER_pdf, PD_pdf])
        # print(response.text) ## if you want ##
        prompt_2 += response.text
    output = model.generate_content(prompt_2)
    print(output.text)