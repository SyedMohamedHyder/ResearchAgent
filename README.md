# 🧠 deepresearch

**deepresearch** is an autonomous AI research assistant built using **OpenAI's Agents SDK** and the **A2A protocol**. It streamlines complex technical and academic research workflows by parsing documents, retrieving relevant information, identifying gaps, and generating research questions — all in an automated and modular fashion.

---

## 🔍 What It Does

The `ResearchCoordinator` orchestrates a pipeline of specialized agents to analyze multiple academic papers and produce foundational elements for a research proposal or paper.

### ✅ Current Multi-Paper Workflow

```
For each paper:
    [1] Summary Generator Agent
           ↓
    [2] Related Work Agent
           ↓
    [3] Gap Identifier Agent

Then (aggregated across all papers):
    [4] Research Question Generator Agent
```

---

## 🤖 Agents Overview

| Agent                      | Description |
|----------------------------|-------------|
| **SummaryGeneratorAgent**  | Extracts structured summaries from each paper, highlighting key contributions, methodologies, and findings. |
| **RelatedWorkAgent**       | Isolates and summarizes the related work sections to understand existing solutions and contexts. |
| **GapIdentifierAgent**     | Analyzes the summaries and related work to identify open problems or unaddressed gaps in the literature. |
| **ResearchQuestionAgent**  | Suggests compelling research questions based on the identified gaps and trends. |

---


## ⚙️ Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your `.env` File

Include your OpenAI API key and any other required environment variables:

```
OPENAI_API_KEY=sk-...
```

### 3. Add Research Papers

Place all your input papers (PDFs) into a folder called `papers/`.

### 4. Run the Pipeline

```bash
python main.py
```

---

## 🚧 Coming Soon

- ✍️ Hypothesis Generator Agent  
- 🛠 Methodology Designer Agent  
- 📈 Evaluation Metrics Agent  
- ✨ Abstract & Title Generator Agent  
- 📚 Citation & Reference Formatter Agent  
- 🔁 Feedback & Iteration Loop

---

## 🧠 Vision

To **automate research planning and ideation**, minimizing the time between reading literature and formulating actionable, publishable insights — while maintaining modularity, traceability, and clarity.

---

## 📄 License

MIT License

---

## 👥 Contributors

- Syed Hyder (Specialist Cloud Developer | Hewlett Packard Enterprise)
