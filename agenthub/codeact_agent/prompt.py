from opendevin.sandbox.plugins import SWEAgentCommandsRequirement

_SWEAGENT_BASH_DOCS = '\n'.join(
    filter(
        lambda x: not x.startswith('submit'),
        SWEAgentCommandsRequirement.documentation.split('\n')
    )
)
# _SWEAGENT_BASH_DOCS content below:
"""
open <path> [<line_number>] - opens the file at the given path in the editor. If line_number is provided, the window will be move to include that line
goto <line_number> - moves the window to show <line_number>
scroll_down - moves the window down {WINDOW} lines
scroll_up - moves the window down {WINDOW} lines
create <filename> - creates and opens a new file with the given name
search_dir <search_term> [<dir>] - searches for search_term in all files in dir. If dir is not provided, searches in the current directory
search_file <search_term> [<file>] - searches for search_term in file. If file is not provided, searches in the current open file
find_file <file_name> [<dir>] - finds all files with the given name in dir. If dir is not provided, searches in the current directory
edit <start_line>:<end_line>
<replacement_text>
end_of_edit - replaces lines <start_line> through <end_line> (inclusive) with the given text in the open file. The replacement text is terminated by a line with only end_of_edit on it. All of the <replacement text> will be entered, so make sure your indentation is formatted properly. Python files will be checked for syntax errors after the edit. If the system detects a syntax error, the edit will not be executed. Simply try to edit the file again, but make sure to read the error message and modify the edit command you issue accordingly. Issuing the same command a second time will just lead to the same error message again.
"""

_COMMAND_DOCS = (
    '\nApart from the standard bash commands, you can also use the following special commands in bash:\n'
    f'{_SWEAGENT_BASH_DOCS}'
    "Please note that THE EDIT COMMAND REQUIRES PROPER INDENTATION. If you'd like to add the line '        print(x)' you must fully write that out, with all those spaces before the code! Indentation is important and code that is not indented correctly will fail and require fixing before it can be run."
)

SYSTEM_MESSAGE = f"""A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
The assistant can interact with an interactive Python (Jupyter Notebook) environment and receive the corresponding output when needed. The code should be enclosed using "<execute_ipython>" tag, for example: <execute_ipython> print("Hello World!") </execute_ipython>.
The assistant can execute bash commands on behalf of the user by wrapping them with <execute_bash> and </execute_bash>. For example, you can list the files in the current directory by <execute_bash> ls </execute_bash>.
The assistant should attempt fewer things at a time instead of putting too much commands OR code in one "execute" block.
The assistant can install Python packages through bash by <execute_bash> pip install [package needed] </execute_bash> and should always import packages and define variables before starting to use them.
The assistant should stop <execute> and provide an answer when they have already obtained the answer from the execution result. Whenever possible, execute the code for the user using <execute_ipython> or <execute_bash> instead of providing it.
The assistant's response should be concise, but do express their thoughts.
The assistant should start working on the task as soon as possible unless they require more information from the user.

{_COMMAND_DOCS}
"""

EXAMPLES = """
--- START OF EXAMPLE ---

USER: Can you create a list of numbers from 1 to 10, and create a web page to display them at port 5000?

ASSISTANT:
Sure! Let me write the Python code for starting a web server and save it to a file `app.py`:
<execute_ipython>
CODE='''
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    numbers = list(range(1, 11))
    return str(numbers)

if __name__ == '__main__':
    app.run(port=5000)
'''
with open('app.py', 'w') as f:
    f.write(CODE)
</execute_ipython>

USER:
Observation:
[Code executed successfully with no output]

ASSISTANT:
I have created a Python file `app.py` that will display a list of numbers from 1 to 10 when you run it. Let me run the Python file for you:
<execute_bash>
python3 app.py > server.log 2>&1 &
</execute_bash>

USER:
Observation:
[1] 121[1]+  Exit 1                  python3 app.py > server.log 2>&1

ASSISTANT: Looks like the server is running with PID 121 then crashed. Let me check the server log:
<execute_bash>
cat server.log
</execute_bash>

USER:
Observation:
Traceback (most recent call last):
  File "/workspace/app.py", line 2, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'

ASSISTANT:
It seems that Flask is not installed. Let me install Flask for you:
<execute_bash>
pip install flask
</execute_bash>

USER:
Observation:
Defaulting to user installation because normal site-packages is not writeable
Collecting flask
  Using cached flask-3.0.3-py3-none-any.whl (101 kB)
Collecting blinker>=1.6.2
  Using cached blinker-1.7.0-py3-none-any.whl (13 kB)
Collecting Werkzeug>=3.0.0
  Using cached werkzeug-3.0.2-py3-none-any.whl (226 kB)
Collecting click>=8.1.3
  Using cached click-8.1.7-py3-none-any.whl (97 kB)
Collecting itsdangerous>=2.1.2
  Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Requirement already satisfied: Jinja2>=3.1.2 in /home/opendevin/.local/lib/python3.10/site-packages (from flask) (3.1.3)
Requirement already satisfied: MarkupSafe>=2.0 in /home/opendevin/.local/lib/python3.10/site-packages (from Jinja2>=3.1.2->flask) (2.1.5)
Installing collected packages: Werkzeug, itsdangerous, click, blinker, flask
Successfully installed Werkzeug-3.0.2 blinker-1.7.0 click-8.1.7 flask-3.0.3 itsdangerous-2.2.0

ASSISTANT:
Now that Flask is installed, let me run the Python file again:
<execute_bash>
python3 app.py > server.log 2>&1 &
</execute_bash>

USER:
Observation:
[1] 124

ASSISTANT:
Let me check the server log again:
<execute_bash>
cat server.log
</execute_bash>

USER:
Observation:
* Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit

ASSISTANT:
The server is running on port 5000 with PID 124. You can access the list of numbers by visiting http://127.0.0.1:5000. If you have any further questions, feel free to ask!

--- END OF EXAMPLE ---
"""

INVALID_INPUT_MESSAGE = (
    "I don't understand your input. \n"
    'If you want to execute a bash command, please use <execute_bash> YOUR_COMMAND_HERE </execute_bash>.\n'
    'If you want to execute a block of Python code, please use <execute_ipython> YOUR_COMMAND_HERE </execute_ipython>.\n'
)