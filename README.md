# KATEKIMA Backend Technical Assesment

## Setting Up the Environment

1. **Create and Activate Python Virtual Environment**  
  Run the following commands to create and activate a Python virtual environment in the `.venv` directory:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
  ```

2. **Install Dependencies**  
  After activating the virtual environment, install the required dependencies using `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## Project Structure

### Assignment 1 Folder
The `Assignment 1` folder contains the following components:

- **LFSR Module**  
  This module includes the `LFSR` class, which implements a Linear Feedback Shift Register (LFSR). The class can be used to generate pseudo-random sequences based on the LFSR algorithm.

- **Main Program**  
  The main program is designed to evaluate the criteria of the LFSR. It demonstrates how to use the `LFSR` class and provides an example of its functionality.

To run the main program, navigate to the `Assignment 1` folder and execute the script:
```bash
python main.py
```

### Assignment 2 Folder
The `Assignment 2` folder contains a backend implementation using Django Rest Framework for a warehouse stock-keeping system.

To get started, navigate to the `Assignment 2` folder and follow the instructions provided in the `README.md` file inside that folder.


---

❕❕❕ Make sure the virtual environment is activated before running the program.