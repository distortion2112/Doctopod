# Doctopod
This project is intended to add some fun to learning and research

Directory Structure:

my-flask-app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   └── config.py
├── uploads/
├── requirements.txt
├── runtime.txt
├── Procfile
├── wsgi.py
└── .env

## Explanation of code 
Sure, here's a brief overview of each function in the referenced Python files:

**File: `app/celery_utils.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| make_celery(app) | Creates a new Celery object and ties the Celery config to the app's config. Wraps all tasks in the context of the Flask application. | app: The Flask application instance | A configured Celery object |

**File: `app/config.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| init_app(app) | This function is defined in each of the Config classes (Config, DevelopmentConfig, TestingConfig, ProductionConfig). It's currently a placeholder and doesn't do anything. | app: The Flask application instance | None |

**File: `app/tasks.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| async_create_outline(file_path) | Creates an outline for a document using OpenAI's API. | file_path: Path to the document file | A dictionary with the outline |
| async_generate_podcast_content(section_text) | Generates detailed podcast content for a section using OpenAI's API. | section_text: Text of the section | A dictionary with the detailed content |
| async_process_outline(outline) | Splits the outline into sections and processes each section. | outline: The outline text | A list of task IDs for each section |
| async_assemble_script(section_task_ids) | Collects the results from each section task and assembles them into a script. | section_task_ids: List of task IDs for each section | A dictionary with the assembled script |

**File: `app/utils.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| async_create_outline(self, file_path) | Creates an outline for a document using OpenAI's API. This function is a Celery task and can be retried if it fails. | self: The Celery task instance, file_path: Path to the document file | A dictionary with the outline |
| async_generate_podcast_content(self, section_text) | Generates detailed podcast content for a section using OpenAI's API. This function is a Celery task and can be retried if it fails. | self: The Celery task instance, section_text: Text of the section | A dictionary with the detailed content |
| create_outline(file_path) | Creates an outline for a document using OpenAI's API. | file_path: Path to the document file | A dictionary with the outline |
| generate_podcast_content(section_text) | Generates detailed podcast content for a section using OpenAI's API. | section_text: Text of the section | A dictionary with the detailed content |

**File: `celery_app.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| debug_task(self) | A debug task that prints the request when it's called. | self: The Celery task instance | None |

**File: `wsgi.py`**

This file doesn't define any functions. It's used to create the Flask application and initialize Celery.

**File: `app/routes.py`**

| Function | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| upload_file() | Handles file upload and starts a task to create an outline for the uploaded file. | None | A JSON response with the task ID |
| outline_status(task_id) | Returns the status of the outline creation task. | task_id: ID of the outline creation task | A JSON response with the task status |
| process_outline(task_id) | Starts a task to process the outline if the outline creation task is successful. | task_id: ID of the outline creation task | A JSON response with the new task ID |
| assemble_script(task_id) | Starts a task to assemble the script if the outline processing task is successful. | task_id: ID of the outline processing task | A JSON response with the new task ID |