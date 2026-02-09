import re
from typing import Optional


def extractTotalProducts(text: str) -> Optional[int]:
    match = re.search(r"Showing\s+\d+\s+of\s+(\d+)", text, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


if __name__ == "__main__":
    raw = """
    <div>
    <span class="actionBar__text"> Showing 18 of 101
    products.
    </span>
    </div>
    """
    print(extractTotalProducts(raw))
