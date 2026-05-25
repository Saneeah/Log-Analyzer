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

total_lines = 0
    clean_errors_count = 0
 
    blank_lines_count = 0
    malformed_or_partial_count = 0
    json_lines_count = 0
    json_errors_count = 0
    multiline_stack_traces_count = 0
 
    parsed_lines_count = 0
    endpoint_times = {}  
 
    error_summary = Counter()
    anomaly_examples = []
 
    print(f"Analyzing: {file_path}...\n")
 
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_num, line in enumerate(file, 1):
            total_lines += 1
            raw_line = line.strip()
 
            if not raw_line:
                blank_lines_count += 1
                continue
            match = LOG_LINE_PATTERN.search(raw_line)
            if match:
                _ip, method, path, _status, time_val, time_unit = match.groups()
                parsed_lines_count += 1
                clean_path = path.split("?")[0]
                key = (method, clean_path)
                response_ms = normalize_to_ms(time_val, time_unit)
                endpoint_times.setdefault(key, []).append(response_ms)
 
                if error_keyword_pattern.search(raw_line):
                    clean_errors_count += 1
                    normalized_error = clean_error_message(raw_line)
                    error_summary[normalized_error or raw_line] += 1
                continue
 
            if raw_line.startswith("{") and raw_line.endswith("}"):
                json_lines_count += 1
                try:
                    data = json.loads(raw_line)
                    json_str = str(data).lower()
                    if error_keyword_pattern.search(json_str):
                        json_errors_count += 1
                      
                        msg = data.get("message") or data.get("error") or raw_line
                        error_summary[f"[JSON] {msg}"] += 1
                except json.JSONDecodeError:
                    malformed_or_partial_count += 1
                    if len(anomaly_examples) < 5:
                        anomaly_examples.append(
                            f"Line {line_num}: Corrupted JSON text"
                        )
                continue
 
            if raw_line.startswith("at ") or line.startswith(("\t", "   ")):
                multiline_stack_traces_count += 1
                if error_keyword_pattern.search(raw_line):
                    clean_errors_count += 1
                    error_summary[f"[Stack Trace Fragment] {raw_line}"] += 1
                continue
 
            if error_keyword_pattern.search(raw_line):
                clean_errors_count += 1

                normalized_error = clean_error_message(raw_line)
 
                if normalized_error:
                    error_summary[normalized_error] += 1
                else:
                    error_summary[raw_line] += 1
                continue

            if len(raw_line) < 10 and not raw_line.isalnum():
                malformed_or_partial_count += 1
                if len(anomaly_examples) < 5:
                    anomaly_examples.append(
                        f"Line {line_num}: Partial/Fragmented text: '{raw_line}'"
                    )
 

if __name__ == "__main__":
    user_path = input("Enter the path to the log file: ").strip()
    analyze_log(user_path)