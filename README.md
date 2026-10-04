# AI4TM - AI for Marketing Masterclass

Content, notebooks, and guides for the AI for Marketing (AI4TM) masterclass — 6 weeks covering AI fundamentals, evaluation, compliance, synthetic data, knowledge graphs, and agentic workflows.

## Getting Started (local, OpenRouter)

This course runs on **your own computer** and talks to models through **OpenRouter**, using the official **OpenAI Python library**.

OpenRouter is one front door. You keep one API key. Behind that door you can pick many models (OpenAI, Google, Anthropic, and others) by changing a model name, not by installing a new library.

The default chat model is `qwen/qwen3-8b`. Embeddings default to `qwen/qwen3-embedding-8b`. Each notebook sets those names in a code cell (`MODEL_NAME`), so you can change them without editing `.env`. These slugs work in more regions than some OpenAI or Gemini names, which can return a 403 “not available in your region” error. Usage on lightweight models is cheap (fractions of a cent per request is typical). Confirm current pricing at [openrouter.ai/models](https://openrouter.ai/models) before a large run, and set a credit limit.

### Quick Start (10 minutes)

1. **Fork this repository** and clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai4tm.git
   cd ai4tm
   ```

2. **Create an OpenRouter API key** at [openrouter.ai/keys](https://openrouter.ai/keys), add a little credit, and set a credit limit at [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits).

3. **Store the key locally**. Create a `.env` file in the project folder (or copy `.env.example`) and fill it in:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```
   The model name is set in each notebook (`MODEL_NAME = "qwen/qwen3-8b"`), not in `.env`. `.env` is already in `.gitignore` so it will not be uploaded to GitHub.

4. **Install [uv](https://docs.astral.sh/uv/)** once, then create this week's environment:
   ```bash
   cd week_2
   uv venv
   uv pip install -r requirements.txt
   ```
   In Cursor or VS Code, open the notebook and choose the `.venv` inside that week folder as the kernel.

5. **Start with the setup guide**:
   [week_2/lesson08_setup_guide.ipynb](week_2/lesson08_setup_guide.ipynb)

### Privacy Note

Anything you send through an API leaves your computer and reaches a third party. Provider terms about training and human review vary by model. **Only use public, synthetic, or anonymized data in this course.** Never send confidential or client data.

## Course Structure

### Week 2: Essential Concepts
**Topics**: Neural networks, attention, tokenization, embeddings
**Approach**: Production failure modes (light theory)
**Content**:
- [Setup Guide (Notebook)](week_2/lesson08_setup_guide.ipynb) - local setup + OpenRouter via the OpenAI Python library
- [Token Cost Guide (Notebook)](week_2/lesson09_token_cost_guide.ipynb) - Estimate cost before running a batch job

### Week 3: Evaluation
**Topics**: Regression, classification, semantic search
**Content**:
- [Evaluation Template (Notebook)](week_3/lesson13_evaluation_template.ipynb) - Accuracy, precision, recall, F1, confusion matrix
- [Human-in-the-Loop Validation (Notebook)](week_3/lesson12_human_in_the_loop.ipynb) - BLEU, ROUGE, LLM-as-judge, and deciding where a person needs to check the model's work

### Week 4: Compliance
**Topics**: AI compliance and regulatory considerations
**Content**:
- **What is the EU AI Act, and Why You Should Care** - Risk categories, provider vs. deployer, the 2026 Digital Omnibus timeline, GDPR overlap (Circle platform)
- **Reviewing Your Own Architecture for Compliance** - A reusable six-step worksheet applying the AI Act criteria to any system you build (Circle platform)
- **Explore a Real-World Use Case** - A real enterprise case study (Starbucks EMEA, built at Monks) read against the AI Act criteria (Circle platform)
- [Setting Up and Protecting Your API Keys (Notebook)](week_4/lesson18_api_key_security.ipynb) - Setup and protection guidelines, keeping keys out of GitHub and out of AI chat prompts
- [Protecting PII When You Use AI (Notebook)](week_4/lesson17_pii_protection.ipynb) - What counts as PII, redacting it before it reaches a prompt, scrubbing a dataframe before an API call
- [Finding Risk Points in an AI Pipeline (Notebook)](week_4/lesson16_pipeline_risk_points.ipynb) - Applying DLP principles across a full pipeline, spot-the-vulnerability exercise

### Week 5: Synthetic Data
**Topics**: Generating and using synthetic data for marketing
**Content**:
- [Synthetic Data Pipeline (Notebook)](week_5/synthetic_data_pipeline.ipynb) - Preprocessing a table, training and tuning a synthetic data generator, and evaluating the synthetic output against the original

### Week 6: Knowledge Graphs
**Topics**: Nodes, edges, and Cypher; turning a set of documents into a graph with an LLM and merging the duplicates it produces; what a graph answers that a table struggles with; GraphRAG and checking whether an answer is actually grounded in the graph
**Content**:
- [Setup: your knowledge graph environment (Notebook)](week_6/setup_guide.ipynb) - Neo4j AuraDB Free signup, connecting the graph database, and a `call_llm()` helper that talks to OpenRouter
- [Building and querying a knowledge graph (Notebook)](week_6/knowledge_graph_pipeline.ipynb) - Extracting entities and relationships from a set of internal documents, merging duplicate entities, loading and querying in Cypher, and GraphRAG with a groundedness check

### Week 7: Agentic Workflows
**Topics**: Search intent taxonomies, clustering a search performance export into content gaps, an agent (tools + a loop) that reads that table, generating a landing page brief and evaluating it against the Week 3 template
**Content**:
- [Building an agentic content pipeline (Notebook)](week_7/agentic_content_pipeline.ipynb) - Rebuilding a compact content-gap table, then a hand-written tool-calling loop (three read-only tools, two visible stopping conditions) that turns it into grounded content recommendations
- [Generating and evaluating a landing page brief (Notebook)](week_7/landing_page_brief_generator.ipynb) - A guardrailed brief generator for one content gap, scored by reusing Week 3's evaluation template against a mix of LLM-judged and objectively-recomputed criteria

## Tools Used

- **Your computer** - Cursor, VS Code, Jupyter Lab, or any local notebook app
- **OpenRouter + the OpenAI Python library** - one key, many models
- **GitHub** - Version control and portfolio

## For Instructors

- All notebooks are designed to run locally
- Students work in their own fork, never as collaborators on this repository — nobody but the instructor team can push to it, forking or not. `main` is branch-protected (PR review required, no force-push or deletion).

## For Students

### Before Each Week
1. Open that week's notebook on your computer
2. Make sure `OPENROUTER_API_KEY` is in `.env`
3. Create that week's environment if you haven't (`cd week_N && uv venv && uv pip install -r requirements.txt`) and select that kernel
4. Run the setup cells

### Tips
- **Save often**: `git add`, `git commit`, `git push` into your fork
- **Experiment**: Try changing code to see what happens
- **Watch your spend**: check pricing at [openrouter.ai/models](https://openrouter.ai/models) and use the token cost guide before a big batch job
- **No real data**: Only use public or made-up data

## Important Notes

- **Never commit API keys** - use `.env` files. See [week_4/lesson18_api_key_security.ipynb](week_4/lesson18_api_key_security.ipynb) for how keys leak and how to catch it.
- Data-use policy (human review, model training) depends on the model behind the OpenRouter slug — check that model's terms, don't assume

## Questions?

Bring them to the office hours or use your course space to post them :)

---

**Ready to learn AI for Marketing? Start here:** [Week 2 Setup Guide](week_2/lesson08_setup_guide.ipynb)
