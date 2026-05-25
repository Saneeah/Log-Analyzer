How to run: Give the exact command(s) or steps to run your project on a fresh machine. If anything needs installing, list it.
Requirements:
- Python 3.7 or higher 

1. Clone the repository:

cd log-analyzer

To test using my own sample log:
2. Use Command: python scripts/generate_log.py
   (This creates `scripts/sample.log`)
   Or use your own log file

3. Use Command: python analyze_log.py
Paste the file path to sample log and press enter to run

Stack choice: Why did you pick this stack/language/framework for this task? What would have been a worse choice and why?
I decided to pick python because it is tailored for text processing and log parsing. The entire nature of this assignment was that the log data was unpredictable instead of always falling under one specific format hence python re module works effectively in this context through allowing me to scrub out dates, and symbols without writing hundreds of lines of code. A worse choice for this could've been C++ although it is faster, the standard regular expression library, regex is very slow and not to mention, managing all the dependencies for c++ takes alot of time.

One real edge case: Describe one specific edge case your code handles correctly. Point to the file and line number. Explain what would happen without that handling.
One of the most destructive inputs for a log analyzer is a truncated JSON write. This edge case is handled safely inside analyze_log.py between Lines 61 and 74: If we didn't protect this block, the analyzer would see that the line starts with { and blindly pass it to json.loads(raw_line). Because the string is cut off mid-sentence, Python's JSON parser would immediately throw a fatal json.decoder.JSONDecodeError. The entire program would crash instantly on line 65. If this happened on line 120,000 of a 500,000-line file, the program would die without producing a report, losing all the data it had already successfully processed.

AI usage: List every place you used AI (which tool, what you asked, what it gave you). For at least one of these, describe something you changed about the AI output and why.
I want to be honest and upfront about my usage for AI in this project. Coming from a background of studying C++ in university and then Javascript for personal projects, I looked into which lanaguge would've been the most appropriate in this context and given the time constraint. From my research I knew Python would've been the best approach but learning the syntax in 48 hours was not resonable for my personal learning style hence I decided to use AI to generate the code however, I tried my best to use my own problem solving and understanding of the fundamental problem to then write accurate prompts and change the output when necessary.
One of the first issues I came across when using Gemini was that initially I simply copy pasted the requirements needed for a successful program and once I ran it, Gemini had hardcoded the program to use a default filename as the test log file instead of prompting the user which was also one of the requirements, that the program should accept a file path. This was not the output that I needed hence I asked Gemini to rewrite this part which then lead to this:
if __name__ == "__main__":
    user_path = input("Enter the path to the log file: ").strip()
    analyze_log(user_path)
and this indeed was what I was looking for hence that issue was fixed.
Another issue that took alot of my time was I kept trying to apply brute force approach to generating a correct solution which only led me to programs that consisted of 700 to 800 lines of code that I didn't understand the logic behind and the output wasn't even close to what the assessment was looking for. This taught me a valuable lesson of breaking down the problem in bits and then asking Gemini to generate the solution to those smaller problems and then combine those solutions to solve a major problem. So I asked Gemini to write me a program that can read the log files in it's standard format and after running it on test data, I then only added on top of the program that got the base requirement right; The new additions being that the program should not crash on malformed lines. 

Honest gap: What's one thing in your submission that isn't good enough, and what would you do to fix it with another day?
The error message normalization in `clean_error_message()` is too aggressive in some cases. After stripping timestamps and response times, it occasionally leaves behind meaningless fragments like "TZ" or "Z" from ISO timestamp suffixes, which appear in the error summary output as "TZ ERROR..." instead of just "ERROR...". This makes the error report slightly harder to read.
