# LCM Web Service

A small Flask web service exposing a single HTTP GET endpoint that computes the **lowest common multiple (LCM)** of two natural numbers.

Built for the Itransition Intern Developer training program (Front-end track) — Task 3.

## Endpoint

```
GET /hesneyhasimaliha_gmail_com?x={x}&y={y}
```

| Param | Type            | Description           |
|-------|-----------------|------------------------|
| `x`   | natural number  | First number           |
| `y`   | natural number  | Second number          |

### Response

Plain text (`Content-Type: text/plain`), containing either:

- the **LCM of `x` and `y`** as a digit string, e.g. `12`
- the literal string `NaN`, if either `x` or `y` is missing, empty, zero, negative, decimal, or otherwise not a natural number

### Examples

```
GET /hesneyhasimaliha_gmail_com?x=4&y=6   →  12
GET /hesneyhasimaliha_gmail_com?x=7&y=11  →  77
GET /hesneyhasimaliha_gmail_com?x=0&y=5   →  NaN
GET /hesneyhasimaliha_gmail_com?x=2.5&y=6 →  NaN
GET /hesneyhasimaliha_gmail_com?x=abc&y=6 →  NaN
```

## How it works

LCM is computed using the identity:

```
LCM(x, y) = (x * y) / GCD(x, y)
```

via Python's built-in `math.gcd`, which handles arbitrarily large integers exactly.

Input validation uses the regex `[1-9][0-9]*` to enforce the natural-number definition ℕ = {1, 2, 3, ...} — rejecting `0`, negatives, decimals, scientific notation, and leading zeros.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

The service starts on `http://localhost:5000`.

## Running tests

```bash
pip install -r requirements.txt pytest
pytest test_app.py -v
```

## Deployment

Configured for [Render](https://render.com) via `Procfile` (`gunicorn app:app`) and `render.yaml`.

## Tech stack

- Python 3
- Flask
- Gunicorn (production WSGI server)
- pytest (testing)
