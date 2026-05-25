from collections import Counter
import json
import os
import re
 
 
def clean_error_message(line):
    
    text = re.sub(r"[\[\(\{\]\)\}]", " ", line)
    text = re.sub(
        r"\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/][A-Za-z]{3}[-/]\d{4}", "", text
    )
    text = re.sub(r"\d{2}:\d{2}:\d{2}(\.\d+)?", "", text)
    text = re.sub(r"\b\d{10,13}\b", "", text)
 
    text = re.sub(r"\b\d+(ms|s)\b", "", text)
    text = re.sub(r"\s-\s", " ", text)
 
    text = re.sub(r"\s+", " ", text).strip()
    return text
 
 
LOG_LINE_PATTERN = re.compile(
    r"""
    (?:
        \d{4}[-/]\d{2}[-/]\d{2}[T ]\d{2}:\d{2}:\d{2}Z?   
      | \d{2}-[A-Za-z]{3}-\d{4}\s\d{2}:\d{2}:\d{2}        
      | \d{10,13}                                           
    )\s+
    ([\d\.]+)\s+                                            
    (GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+             
    (/\S*)\s+                                               
    (-|\d{3})\s+                                            
    (\d+(?:\.\d+)?)(ms|s|)                                  
    """,
    re.VERBOSE
)

def normalize_to_ms(value, unit):
    v = float(value)
    if unit == "s":
        return v * 1000
    return v  
 
 
def analyze_log(file_path):

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
 
    error_keyword_pattern = re.compile(
        r"(error|exception|fail|critical|fatal)", re.IGNORECASE
    )
 

if __name__ == "__main__":
    user_path = input("Enter the path to the log file: ").strip()
    analyze_log(user_path)