# Diff Tool

A tool that compares a Comestri product export against the full product catalogue on the Feedonomics SFTP, and produces an Excel report highlighting what's missing and what's changed.

## What it does

1. Accepts a Comestri export (`.zip` containing XML files)
2. Downloads the full catalogue from the SFTP (`style.xml.gz`, `style-colour.xml.gz`, `sku.xml.gz`)
3. Parses both into a structured table, extracting all standard fields, custom attributes, and variation data
4. Generates a three-tab Excel workbook:
   - **Report** — product set summary (found/missing per level) and per-column diff stats
   - **Diff Details** — row-level differences between the Comestri export and SFTP values
   - **Missing Products** — products present in the Comestri export but absent from the SFTP

The workbook is saved to `~/Downloads` and also uploaded to `/incoming/diff_reports` on the SFTP.

## Setup

### Requirements

- Python 3.10+

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install lxml pandas paramiko python-dotenv openpyxl
```

### Configure credentials

Copy `.env.example` to `.env` and fill in the SFTP credentials:

```bash
cp .env.example .env
```

```
SFTP_HOST=
SFTP_PORT=22
SFTP_USERNAME=
SFTP_PASSWORD=
```

## Usage

```bash
source .venv/bin/activate
python diff.py
```

You will be prompted for:

1. **Comestri export file path** — the `.zip` file to diff
2. **Max differences per column** — caps rows in the Diff Details tab per column (press Enter for no limit)

## Extracting a single product

`extract_product.py` pulls one `<product>` node out of a catalogue XML so you can inspect it.

```bash
source .venv/bin/activate
python extract_product.py
```

You will be prompted for:

1. **XML or ZIP file path** — an `.xml` file, or a `.zip` (nested zips are searched too, e.g. a Comestri export)
2. **Product ID** — matched against the `product-id` attribute

The node is saved to `~/Downloads/product_{product_id}.xml` and the script prints which file it was found in. If the ID appears in more than one file, only the first match is written.

## Product levels

Products are classified as follows:

| Level | Rule |
|-------|------|
| `style` | Contains a `<variations>` element |
| `sku` | Product ID matches `^\d{13,}-` |
| `style-colour` | Product ID contains a hyphen (all other cases) |

## Output

| File | Location |
|------|----------|
| `report_{timestamp}.xlsx` | `~/Downloads` |
| `report_{timestamp}.xlsx` | `/incoming/diff_reports` on SFTP |
| `product_{product_id}.xml` (from `extract_product.py`) | `~/Downloads` |
