# GraphQL to REST Workflow Automation

This project automates the process of fetching data from a GraphQL API, posting specific data to a REST API, and saving all the data into a CSV file.
It includes error handling for common scenarios and is written in Python.

---

## Features

1. Fetch country data from the Countries GraphQL API.
2. Post details of a selected country to a REST API.
3. Save all fetched country data to a CSV file.
4. Handle common errors like `403 Forbidden` and `500 Internal Server Error` gracefully.
5. Automates the entire workflow with retries and exponential backoff for robustness.

---

## Prerequisites

- Python 3.6 or higher
- `requests` library for making HTTP requests
- No additional setup is required as it uses the `csv` module available in Python's standard library.

Install the `requests` library if not already installed:
```bash
pip install requests
