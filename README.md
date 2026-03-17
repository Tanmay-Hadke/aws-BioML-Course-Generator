# 🧬 BioML: Multi-Agent Bioinformatics Course Generator

BioML is a full-stack, cloud-native MLOps pipeline that orchestrates multiple AI agents to generate university-level bioinformatics curricula. It features automated code validation and a real-time monitoring dashboard.

## 🚀 The Pipeline Explained

The system follows a "Chained Agentic Workflow" managed by **AWS Step Functions**:

1.  **Agent 1 (Curriculum Architect):** Analyzes the topic and target audience to generate a structured 3-module syllabus.
2.  **Agent 2 (Lead Professor):** Takes the syllabus and expands it into detailed, technical lecture notes.
3.  **Agent 3 (Lab Instructor):** Generates functional Python code snippets for practical implementation.
4.  **Agent 4 (MLOps Validator):** Performs a "Sanity Check" by compiling the generated code to catch syntax errors before storage.
5.  **Persistence:** The validated course is stored in **Amazon DynamoDB** with a unique `course_id`.



## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3 (Grid/Flexbox), JavaScript (Fetch API)
* **Orchestration:** AWS Step Functions
* **Compute:** AWS Lambda (Python 3.12)
* **Database:** Amazon DynamoDB
* **API Layer:** AWS API Gateway (REST)
* **Security:** AWS IAM (Least Privilege Principal)

## 🔧 Installation & Setup

### 1. Backend Setup
* Deploy the 4 Agent Lambdas provided in the `/backend` folder.
* Ensure the Step Function IAM Role has `lambda:InvokeFunction` and `dynamodb:PutItem` permissions.
* Create a DynamoDB table named `BioML-Courses` with `course_id` as the Partition Key (String).

### 2. Orchestration
* Import the `step_function.json` into AWS Step Functions.
* Update the Lambda ARNs to match your deployed functions.

### 3. Frontend
* Open `frontend/index.html`.
* Update the `TRIGGER_API_URL` and `FETCH_API_URL` with your API Gateway Invoke URLs.

## 📊 MLOps Features
* **Automated Validation:** Every generated code snippet is tested for syntax errors.
* **Side-by-Side Monitoring:** Compare syllabus and code implementation instantly.
* **Input Sanitization:** Uses `.trim()` and regex cleaning to ensure database integrity.