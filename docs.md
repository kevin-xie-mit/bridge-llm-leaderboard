
<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/lsCIUxFkADB-Wf9cteeB4.png" alt="Leaderboard Image 1" width="200"/>

<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/E-WF4uJB0GzplioJkWh5v.webp" alt="Leaderboard Image 2" width="200"/>

<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/xQqbGXh0y6zIV78Cw6Vpq.png" alt="Leaderboard Image 3" width="800"/>


## 📜 Background
Recent advances in **Large Language Models (LLMs)** have demonstrated transformative potential in improving healthcare delivery and clinical research. By combining extensive pretraining with supervised instruction tuning across diverse tasks, LLMs excel in natural language understanding, generation, and reasoning. These capabilities allow LLMs to serve as versatile, general-purpose medical assistants.

Despite this promise, concerns remain around the **reliability and clinical validity** of LLM-generated outputs. Real-world contexts often involve unstructured, multilingual text from **electronic health records (EHRs)**, and require support for tasks like phenotype identification and event extraction that remain underexplored. Moreover, the scarcity of **multilingual benchmarks** further limits the global applicability of LLMs in medicine.

To address these challenges, we introduce the ***largest multilingual clinical benchmark*** to date, **BRIDGE (Benchmarking Large Language Models in Multilingual Real-world Clinical Text Understanding)**, evaluating 52 LLMs on:

- **87 clinical tasks**
- **9 languages**
- **1M+ clinical samples**

## 🌍 Key Features

Our benchmark spans a wide range of document types and clinical tasks, including classification, event extraction, and generation. It further supports three inference strategies: **zero-shot**, **few-shot**, and **chain-of-thought (CoT)** prompting. We evaluated **52 LLMs**, including general-purpose, open-source, proprietary, and medical-domain models.


- **Multilingual Data**: Clinical tasks in **9 languages** for global relevance.
- **Diverse Clinical Documents**: Notes, summaries, radiology reports, and more.
- **Multiple NLP Tasks**: Classification, extraction, QA, summarization, etc.
- **Evaluation Modes**:
  - **Zero-shot**
  - **Few-shot**
  - **Chain-of-Thought (CoT)** reasoning


## 🏆 BRIDGE Leaderboard

To support ongoing evaluation, we introduce our **BRIDGE Leaderboard**, which provides:

- Easy visualizations
- Side-by-side comparisons
- Continuous tracking of LLM performance across tasks, languages, and evaluation strategies

This leaderboard empowers researchers and clinicians to make informed decisions and track model progress over time.


## 📚 Citation

If you use this benchmark in your research or development, please cite:

```bibtex
@article{BRIDGE2025,
  title     = {PAPER TITLE},
  author    = {Your Name and Contributors},
  year      = {2025},
  journal   = {Your Journal or Conference},
}

