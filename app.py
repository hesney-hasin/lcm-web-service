import math
import re
import os
from flask import Flask, request, Response

app = Flask(__name__)

EMAIL_SUFFIX = "hesneyhasimaliha_gmail_com"


def is_natural(val: str) -> bool:
    """
    Returns True iff `val` is a string that represents a natural number (ℕ = {1, 2, 3, …}).

    Rejects:
      - None / empty string
      - Strings with a decimal point ("1.0", "3.14")
      - Scientific notation ("1e5")
      - Negative numbers ("-1")
      - Leading zeros ("01", "007")
      - Zero itself ("0")
      - Any non-digit character
    """
    if not val:
        return False
    # [1-9] guarantees ≥ 1 and no leading zeros; [0-9]* allows further digits
    return bool(re.fullmatch(r"[1-9][0-9]*", val))


def lcm(x: int, y: int) -> int:
    """
    Computes LCM(x, y) using the identity:
        LCM(x, y) = (x * y) / GCD(x, y)

    Python's math.gcd is exact for arbitrarily large integers (no overflow).
    Integer floor-division is used to keep the result an int.
    """
    return x * y // math.gcd(x, y)


@app.route(f"/{EMAIL_SUFFIX}")
def lcm_endpoint():
    x_str = request.args.get("x", "")
    y_str = request.args.get("y", "")

    if not is_natural(x_str) or not is_natural(y_str):
        return Response("NaN", mimetype="text/plain")

    result = lcm(int(x_str), int(y_str))
    return Response(str(result), mimetype="text/plain")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
