import json
import uuid
import openai
import sys
import os
import xml.etree.ElementTree as ET
import re
import datetime
import time
import config

# ToDo: Macro F1
# API Key for GPT should look like this openai.api_key = "My_key"
openai.api_key = config.API_KEY


# Loading the Prompt from the text file
def loadPrompt():
    prompt = "prompt_GermEval.txt"
    if os.path.exists(f"messages/{prompt}"):
        file = open(f"messages/{prompt}", "r", encoding="utf-8")
        prompt = file.read()
    else:
        print("Error Reading Prompt")
    # print(prompt)
    return prompt


# load the json schema
def loadFunction():
    json_file = "json_schema.json"
    if os.path.exists(f"messages/{json_file}"):
        file = open(f"messages/{json_file}", "r")
        function = json.load(file)
    else:
        print("No function schema found")
    # print(f"function:{function} \n")
    return function


# Call GPT with every data from the xml files
def chatGPTcall():
    prompt = loadPrompt()
    function = loadFunction()
    # name_list = ["MobASA_Test_Clean_1.xml", "MobASA_Test_Clean_2.xml", "MobASA_Test_Clean_3.xml", "MobASA_Test_Clean_4.xml", "MobASA_Test_Clean_5.xml", "MobASA_Test_Clean_6.xml", "MobASA_Test_Clean_7.xml", "MobASA_Test_Clean_8.xml", "MobASA_Test_Clean_9.xml", "MobASA_Test_Clean_10.xml"]
    name_list = ["GermEval_Test_Clean_1.xml", "GermEval_Test_Clean_2.xml", "GermEval_Test_Clean_3.xml", "GermEval_Test_Clean_4.xml", "GermEval_Test_Clean_5.xml", "GermEval_Test_Clean_6.xml", "GermEval_Test_Clean_7.xml", "GermEval_Test_Clean_8.xml", "GermEval_Test_Clean_9.xml", "GermEval_Test_Clean_10.xml"]
    # name_list = ["StudyCheck_Test_clean.xml"]
    # name_list = ["SemEval_Test_Clean.xml"]
    # name = name_list[0]
    for name in name_list:
        input_dict = loadCorpus(name)

        for key in input_dict:
            # handle too much requests with a wait time
            time.sleep(1)
            user_input = input_dict[key]
            # print(f"User Input: \n{user_input} \n")
            try:
                response = openai.ChatCompletion.create(
                    # model="gpt-4",
                    model="gpt-3.5-turbo",
                    temperature=0,
                    messages=[{"role": "system", "content": prompt},
                              {"role": "user", "content": user_input}],
                    # The [] are absolutely needed. This error took 2 hours.
                    functions=[function],
                    function_call="auto"
                )
            # these exception handlers are from "Comparing ChatGPT to Human Raters and Sentiment Analysis Tools
            # for German Children’s Literature repo"
            except openai.error.APIError as e:
                # Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                writeError("APIError", key)
                continue
            except openai.error.APIConnectionError as e:
                # Handle connection error here
                print(f"Failed to connect to OpenAI API: {e}")
                writeError("APIConnectionError", key)
                continue
            except openai.error.RateLimitError as e:
                # Handle rate limit error (we recommend using exponential backoff)
                print(f"OpenAI API request exceeded rate limit: {e}")
                writeError("RateLimitError", key)
                continue
            except openai.error.ServiceUnavailableError as e:
                # Handle service unavailable error
                print(f"OpenAI API service is unavailable: {e}")
                writeError("ServiceUnavailableError", key)
                continue
            except openai.error.Timeout as e:
                # Handle timeout error
                print(f"OpenAI API timed out: {e}")
                writeError("Timeout", key)
                continue
            except Exception as e:
                # catch all other exceptions, print exception error
                exception_type = sys.exc_info()[0]
                print("An exception of type", exception_type, f"occurred. {e}")
                writeError("Exception", key)
                continue

            # json_response = json.loads(response.choices[0].message.function_call.arguments)
            # print(response)
            if hasattr(response.choices[0].message, 'function_call'):
                json_answer = response.choices[0].message.function_call.arguments
                answer = json.loads(json_answer)
                finish_reason = response["choices"][0]["finish_reason"]
                tokens = response["usage"]["total_tokens"]

                print(f"Total Amount of Tokens per request: {tokens}.")
                # print(f"Full response: \n{response}")
                print(f"Response json: \n{answer}")

                if (finish_reason != "function_call" and finish_reason != "stop"):
                    writeError("Finish reason Error", key)
                    print(f"Error at {key} finish reason is not function_call or stop")

                saveResponse(json_answer, key, user_input)
            else:
                print(f"Error at {key}, no response")
                writeError("Request didn't work, no JSON as return", key)


# print error messages in a file.txt
def writeError(message, key):
    current_timestamp = datetime.datetime.now()
    error_message = "Error at " + str(key) + " at Time " + str(current_timestamp) + " with error " + message + "\n"
    with open("output/error_messages_GermEval_Minimal.txt", "a") as file:
        file.write(error_message)


# Source Code: https://community.openai.com/t/api-response-encoding-bug-utf-8-utf-16/622103/2
# Converts a dict into a string and replace all wrong encodings. Converts the string back into a dict
def fix_encoding(response_dict):
    response_string = str(response_dict)
    # Define the mapping of incorrect two-character sequences to the correct characters
    correction_map = {
        'Ã\xa0': 'à', 'Ã¨': 'è', 'Ã©': 'é', 'Ã¬': 'ì', 'Ã²': 'ò', 'Ã³': 'ó', 'Ã¹': 'ù',
        'Ã¤': 'ä', 'Ã¶': 'ö', 'Ã¼': 'ü', 'ÃŸ': 'ß',
        'Ã¡': 'á', 'Ã­': 'í', 'Ã±': 'ñ', 'Ãº': 'ú',
        'Ã¢': 'â', 'Ãª': 'ê', 'Ã«': 'ë', 'Ã®': 'î', 'Ã¯': 'ï', 'Ã´': 'ô', 'Ã»': 'û', 'Ã§': 'ç'
    }
    # Create a regular expression from the map
    regex = re.compile("(%s)" % "|".join(map(re.escape, correction_map.keys())))

    # For each match, look-up corresponding value in dictionary
    response_string_updated = regex.sub(lambda mo: correction_map[mo.string[mo.start():mo.end()]], response_string)

    response_dict_updated = eval(response_string_updated)

    return response_dict_updated


# save the response as a json file
def saveResponse(answer, key, user_input):
    new_uuid = uuid.uuid4()
    file_path = "prediction/" + str(new_uuid) + ".json"

    json_answer = json.loads(answer)
    json_update = {
                    "id": key,
                    "text": user_input,
                    **json_answer
                    }

    # updated_json type dict
    corrected_dict = fix_encoding(json_update)

    # save the json file
    with open(file_path, "w", encoding="utf-8") as outputFile:
        json.dump(corrected_dict, outputFile, ensure_ascii=False, indent=4)
        print("Response saved!")


# Loading the corpus from the xml file and making a dict with the id as key and the user text as value
def loadCorpus(name):
    corpus_dict = {}
    if os.path.exists(f"input/{name}"):
        tree = ET.parse(f"input/{name}")
        root = tree.getroot()
        for entry in root.findall("Document"):
            identifier = entry.get("id")
            user_text = entry.find("text").text

            corpus_dict.update({identifier: user_text})
    return corpus_dict


def main():
    # loadPrompt()
    # loadGermEval()
    chatGPTcall()


if __name__ == '__main__':
    sys.exit(main())
