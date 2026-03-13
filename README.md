# 🗓️ Timeline Creator
**Stop building project roadmaps in PowerPoint. Generate them from data.**

This tool automates the creation of high-quality, staggered project timelines using Python. It handles Fiscal Year (FY) logic (April-March), quarterly shading, and long-term (5-year) spans without the manual alignment headaches of slide decks.

![Project Roadmap Sample](test_data%20-%205%20year_2026-03-13_15-58.png)

## ✨ Features
* **Automatic Staggering:** Prevents label overlap by alternating vertical heights.
* **FY/Quarterly Shading:** Dynamically shades backgrounds based on Fiscal Year logic (April start).
* **Data-Driven:** Update a simple CSV, and your roadmap regenerates instantly.
* **Dynamic Naming:** Output images are automatically named based on your source file and the current timestamp.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
