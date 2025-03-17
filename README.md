![Banner Description](https://repository-images.githubusercontent.com/945531906/b6d191a7-2a54-46d1-af23-ed1a348d8048)
# Mellisa: Web Parameter Crawling Tool

**Discover potential vulnerable parameters underneath web pages**
# Description
This Python script scans web pages to extract potential URL parameters, form fields, and query strings that could be vulnerable to SQL injection attacks. It automates reconnaissance by crawling target websites, identifying input fields, and logging discovered parameters for security analysis and penetration testing.

**What the tool can solve:**

**1. Identifying Injection Points** – It automates the discovery of URL parameters, form fields, and hidden inputs that could be exploited for SQL injection.

**2. Reducing Manual Effort** – Security researchers and penetration testers don’t need to manually inspect pages; the script quickly gathers potential injection points.**

**3. Assisting in Automated Exploitation** – The extracted parameters can be fed into SQL injection testing tools like sqlmap for further exploitation.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

# Installation 

1. Clone the repository:
   - git clone https://github.com/yel1337/mellisa.git
2. Go to project's directory:
   - cd Mellisa
3. Install dependencies:
   - pip install -r requirements.txt

# Usage 

- Supports both "https://" and "http://" websites
- Running the script: python3 mellisa.py <url>
- Example:
      python3 mellisa.py https://www.google.com/
  
Optional Arguments:
    
    --h   --HELP    Show help message

# License 

This project is licensed under the Apache License 2.0 
      
   A permissive license whose main conditions require preservation of copyright and license notices. Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
