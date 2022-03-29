# FastAPI Currency Converter

### Converts Values From One Currency To Another


#### Installation
The implementation is based on FastAPI --A Python API Framework with speed matching GO programming language.
To run the program, you need FastAPI installed. And to have FastAPI installed, you need to have python installed.

#### Install Python
If you don't have python, goto https://python.org/download and follow the instructions to install python version 3.

#### Clone the Repository
Open your terminal or shell with git installed and run `git clone https://github.com/honeson/fastapi-currency-converter-task.git` in same folder/directory as you would want the project to live. Then `cd` into the cloned directory.

### NOTE:
The Secret key needed to be able to connect to the API provider is in `.example_env` file. What this means is that you need to copy it into `.env` file in the project root directory. If you intend to continue using the programme, you should head over to: `https://currencyapi.com/` and signup to get your own free API_KEY.

##### Create Virtual Environment
To install the dependencies required to run this program, first create a virtual environment using venv. This should be done in same folder as where you cloned the repo into. Then with python and venv already installed, run `python -m venv venv`. This will create a virtual environment called venv for you.

#### Activate Environment
Next, activate the virtual environment by running, `venv\scripts\activate` (for windows users).

#### Install Dependencies
While still in the activated environment, run `pip install -r requirements.txt`. This will install all required dependencies for the program to run.

Once the program is up and running, navigate to: `http://127.0.0.1:8700` on your browser to see the program in action.

#### Test the converter
To see the inbuilt browseable API documentation and test the how the pogram runs, navigate to: `http://127.0.0.1:8700/docs` for swagger docs or `http://127.0.0.1:8700/redoc` for Redoc style documentation.

#### Thanks!
Now that you have tested the API, do enjoy it and leave feedback.
