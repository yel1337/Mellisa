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
- [Testing Domains and Best Practices](#testing-domains-and-best-practices)
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
*From the root directory do*
```bash
cd mellisa
```

*Inside the directory, make the shell script executable by running:*
```bash
chmod +x mellisa.sh
```

*Run the crawler from the project root (while the virtual environment is active):*

  ```bash
  ./mellisa.sh <url>
  ```

  Example:

  ```bash
  ./mellisa.sh https://www.google.com/
  ```

## Testing Domains and Best Practices

### ✅ Safe & Legal Test Domains

For testing Mellisa's functionality, use these intentionally vulnerable sites designed for security testing:

1. **http://testphp.vulnweb.com** - Acunetix test site (tested, works but found no params on homepage)
2. **http://demo.testfire.net** - Banking demo site
3. **http://zero.webappsecurity.com** - Zero Bank demo
4. **https://juice-shop.herokuapp.com** - OWASP Juice Shop online

### 🎯 Best Practices for Parameter Discovery

For effective parameter discovery testing:

1. **Use local vulnerable apps** like DVWA or bWAPP for comprehensive testing
2. **Target specific pages with known parameters** (search pages, login forms, etc.)
3. **Always ensure you have explicit permission** before testing any website

### Understanding Tool Behavior

The tool is working correctly when it:
- Validates URLs properly
- Respects/ignores robots.txt as configured
- Creates output files in the `output/` directory
- Handles pages with/without parameters appropriately

> **Note:** The warning "Page might not contain any parameter/s" is expected when scanning pages without URL parameters (common on homepages). Mellisa is designed to find pages with query strings containing potential injection points.

### Optimal Target Pages

For best results, target pages with forms or known parameters like:
- Search pages (`/search.php?q=test`)
- Product listings (`/products.php?category=1`)
- User profiles (`/user.php?id=123`)
- Login forms (`/login.php?redirect=/home`)
- API endpoints (`/api/v1/users?limit=10`)

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
./mellisa.sh http://localhost:8888/
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
