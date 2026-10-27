import io
import os
import sys
import zipfile

from lxml import etree

CATALOG_NS = "http://www.demandware.com/xml/impex/catalog/2006-10-31"
PRODUCT_TAG = f"{{{CATALOG_NS}}}product"

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")


def _search_stream(stream, product_id):
    """Stream through one XML and return the matching <product> element, or None."""
    for _, elem in etree.iterparse(stream, events=("end",), tag=PRODUCT_TAG, huge_tree=True):
        if elem.get("product-id") == product_id:
            return elem
        # Free memory for products we've already passed over.
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    return None


def find_product(source, product_id, label=None):
    """Search an XML file, or a (possibly nested) zip of XML files.

    `source` is a path or file-like object. Returns (element, where_found) or (None, None).
    """
    label = label or str(source)
    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as zf:
            for name in sorted(zf.namelist()):
                if name.endswith("/") or name.startswith("__MACOSX"):
                    continue
                lower = name.lower()
                if lower.endswith(".zip"):
                    inner = io.BytesIO(zf.read(name))
                elif lower.endswith(".xml"):
                    inner = zf.open(name)
                else:
                    continue
                found, where = find_product(inner, product_id, f"{label}/{name}")
                if found is not None:
                    return found, where
        return None, None

    if hasattr(source, "seek"):
        source.seek(0)
    try:
        return _search_stream(source, product_id), label
    except etree.XMLSyntaxError as e:
        print(f"Skipping {label}: could not parse XML ({e})")
        return None, None


def main():
    xml_path = os.path.expanduser(input("Enter XML or ZIP file path: ").strip().strip("'\""))
    if not os.path.isfile(xml_path):
        sys.exit(f"File not found: {xml_path}")

    product_id = input("Enter product ID: ").strip()
    if not product_id:
        sys.exit("No product ID entered.")

    product, where = find_product(xml_path, product_id)

    if product is None:
        sys.exit(f"Product '{product_id}' not found in {xml_path}")

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    out_path = os.path.join(DOWNLOADS_DIR, f"product_{product_id}.xml")
    etree.ElementTree(product).write(
        out_path, pretty_print=True, xml_declaration=True, encoding="UTF-8"
    )
    print(f"Found in {where}")
    print(f"Wrote product node to {out_path}")


if __name__ == "__main__":
    main()
