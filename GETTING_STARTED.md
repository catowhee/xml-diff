# Getting Started

This guide will walk you through everything you need to run the diff tool on a Mac, even if you've never used Python before.

---

## Step 1: Install Python

1. Open **Terminal** (press `Cmd + Space`, type "Terminal", hit Enter)
2. Check if Python is already installed by typing:
   ```
   python3 --version
   ```
   If you see something like `Python 3.11.4`, you're good — skip to Step 2.

3. If Python isn't installed, the easiest way is via the official installer:
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click **"Download Python 3.x.x"** (the big yellow button)
   - Open the downloaded `.pkg` file and follow the installer steps
   - Once done, run `python3 --version` in Terminal to confirm it worked

---

## Step 2: Get the code

Clone the repository from GitHub. In Terminal, navigate to wherever you'd like to keep the project (e.g. your Documents folder):

```bash
cd ~/Documents
git clone https://github.com/catowhee/xml-diff.git
cd xml-diff
```

> If you don't have Git installed, Terminal will prompt you to install it the first time you run `git`. Just follow the prompt.

---

## Step 3: Set up the project

You only need to do this once.

### 3a. Create a virtual environment

A virtual environment keeps this project's dependencies separate from anything else on your Mac.

```bash
python3 -m venv .venv
```

### 3b. Activate it

```bash
source .venv/bin/activate
```

Your Terminal prompt will change to show `(.venv)` at the start — this means it's active.

### 3c. Install dependencies

```bash
pip install lxml pandas paramiko python-dotenv openpyxl
```

This downloads the libraries the tool needs. It only takes a minute.

---

## Step 4: Configure credentials

The tool needs SFTP credentials to connect to the server. These are stored in a file called `.env` in the project folder.

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in a text editor (TextEdit works, or any editor you have):
   ```bash
   open -e .env
   ```
3. Fill in the values — your colleague (JP) will provide these:
   ```
   SFTP_HOST=
   SFTP_PORT=22
   SFTP_USERNAME=
   SFTP_PASSWORD=
   ```
4. Save and close the file.

> **Important:** Never share or commit the `.env` file — it contains passwords. It's already excluded from Git for this reason.

---

## Step 5: Run the tool

Each time you want to run the tool:

**1. Open Terminal and navigate to the project folder:**
```bash
cd ~/Documents/<repo-folder>
```

**2. Activate the virtual environment:**
```bash
source .venv/bin/activate
```
> You need to do this every time you open a new Terminal window.

**3. Run the script:**
```bash
python diff.py
```

**4. Follow the prompts:**
- **Comestri export file path** — drag and drop the `.zip` file into Terminal, or type the full path (e.g. `/Users/yourname/Downloads/export.zip`)
- **Max differences per column** — enter a number like `50` to cap the diff details, or press Enter to include everything

**5. Find your report:**

Once the script finishes, the Excel report will appear in your **Downloads** folder, named something like `report_20260712_143000.xlsx`.

---

## Troubleshooting

**"command not found: python3"**
Python isn't installed. Go back to Step 1.

**"No module named 'paramiko'" (or similar)**
The virtual environment isn't active. Run `source .venv/bin/activate` and try again.

**"(.venv)" disappeared from my prompt**
You opened a new Terminal window. Run `source .venv/bin/activate` again.

**SFTP connection errors**
Double-check the credentials in your `.env` file. Make sure there are no extra spaces around the `=` sign.
