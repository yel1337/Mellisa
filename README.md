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

## Quick Functional Test (w/NetSPI XPath-Injection Lab)

This walk-through spins up NetSPI’s *Path Injection Weakness* demo locally, runs Mellisa against it, and inspects the JSON output.

### 1. Set up the test target  

```bash
# Clone the lab (or your own fork)
git clone https://github.com/NetSPI/path-injection-weakness-lab.git
cd path-injection-weakness-lab

# Start the vulnerable app (using Docker Compose)
docker compose up -d
# The lab now listens on http://localhost:8888/
```
### 2. Run Mellisa against the lab

```bash
# From a second terminal in the Mellisa repo root
source mellisa-venv/bin/activate
python mellisa.py http://localhost:8888/
```

Mellisa crawls the target and writes results to:
```mellisa/output/   # relative to mellisa.py```

### 3. Review Results

Open the JSON file in your editor or run:

```bash
# files are saved as:  output/<targethost>_<port>.json | <targetdomain>_<directory>.json
jq . output/localhost_8888.json
```
The JSON should look something like this:
```json
[
  {
    "item_param": [
      "/css/site.css?v=AKvNjO3dCPPS0eSU1Ez8T2wI280i08yGycV9ndytL-c",
      "/BookSearchApp.styles.css?v=OCvwvqV0ZzKYOYPf5YqKGSuS_ZPHLCdiAKW156PLJao"
    ]
  },
  {
    "item_param": [
      "/css/site.css?v=AKvNjO3dCPPS0eSU1Ez8T2wI280i08yGycV9ndytL-c",
      "/BookSearchApp.styles.css?v=OCvwvqV0ZzKYOYPf5YqKGSuS_ZPHLCdiAKW156PLJao"
    ]
  }
]
```

# License 

This project is licensed under the Apache License 2.0 
      
   A permissive license whose main conditions require preservation of copyright and license notices. Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
