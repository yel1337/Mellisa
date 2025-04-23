![Banner Description](https://repository-images.githubusercontent.com/945531906/2ab5c057-011f-4548-9b9a-3d81b777ec4c)
# Mellisa: Web Parameter Crawling Tool

**Discover potential vulnerable parameters underneath web pages**
# Description
This Python script scans web pages to extract potential URL parameters, form fields, and query strings that could be vulnerable to SQL injection attacks. It automates reconnaissance by crawling target websites, identifying input fields, and logging discovered parameters for security analysis and penetration testing.

**What the tool can solve:**

**1. Identifying Injection Points** – It automates the discovery of URL parameters, form fields, and hidden inputs that could be exploited for SQL injection.

**2. Reducing Manual Effort** – Security researchers and penetration testers don’t need to manually inspect pages; the script quickly gathers potential injection points.

**3. Assisting in Automated Exploitation** – The extracted parameters can be fed into SQL injection testing tools like sqlmap for further exploitation.

> **Note:** The script now resolves `wordlist.txt` dynamically via `pathlib`, so no hard‑coded paths are required.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

# Installation

```bash
# 1. Clone the repository
git clone https://github.com/yel1337/mellisa.git
cd mellisa

# 2. (Recommended) Create and activate a virtual environment
python3 -m venv mellisa-venv
source mellisa-venv/bin/activate     # Windows: mellisa-venv\Scripts\activate

# 3. Upgrade pip (optional but encouraged)
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt
```

> **Why a virtual‑env?**  
> Kali Linux and other security‑oriented distros preload tools (e.g., `mitmproxy`, `theHarvester`) that pin specific package versions.  
> Installing Mellisa in an isolated environment prevents version conflicts and keeps system tools intact.

# Usage

*Run the crawler from the project root (while the virtual environment is active):*

  ```bash
  python mellisa.py <url>
  ```

  Example:

  ```bash
  python mellisa.py https://www.google.com/
  ```

#### Docker (optional)

```bash
docker build -t mellisa .
docker run --rm mellisa https://www.example.com/
```

Optional Arguments:
    
    --h   --HELP    Show help message

# License 

This project is licensed under the Apache License 2.0 
      
   A permissive license whose main conditions require preservation of copyright and license notices. Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
