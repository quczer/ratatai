# ratatai

## Setting up the Development Environment

To set up a virtual environment for this project, follow these steps:

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install .
   ```

   Alternatively, if you want to install the dependencies listed in `pyproject.toml` without installing the package itself, you can use:
   ```bash
   pip install -e .[dev]
   ```

Make sure to deactivate the virtual environment when you're done working by running `deactivate`.