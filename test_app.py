import pytest
from app import app, is_natural, lcm


# ─── Unit: is_natural ────────────────────────────────────────────────────────

class TestIsNatural:
    def test_basic_positive(self):
        assert is_natural("1")
        assert is_natural("2")
        assert is_natural("100")
        assert is_natural("999999999999999999")  # arbitrary precision

    def test_zero_is_not_natural(self):
        assert not is_natural("0")

    def test_negative_is_not_natural(self):
        assert not is_natural("-1")
        assert not is_natural("-100")

    def test_decimal_is_not_natural(self):
        assert not is_natural("1.0")
        assert not is_natural("3.14")
        assert not is_natural("2.")

    def test_scientific_notation_is_not_natural(self):
        assert not is_natural("1e5")
        assert not is_natural("1E5")

    def test_leading_zeros_are_not_natural(self):
        assert not is_natural("01")
        assert not is_natural("007")

    def test_non_numeric_strings(self):
        assert not is_natural("abc")
        assert not is_natural("one")
        assert not is_natural("")
        assert not is_natural(None)
        assert not is_natural(" 1")   # leading space
        assert not is_natural("1 ")   # trailing space


# ─── Unit: lcm ───────────────────────────────────────────────────────────────

class TestLcm:
    def test_basic(self):
        assert lcm(4, 6) == 12
        assert lcm(3, 5) == 15
        assert lcm(1, 1) == 1

    def test_same_number(self):
        assert lcm(7, 7) == 7

    def test_one_is_factor_of_other(self):
        assert lcm(3, 9) == 9
        assert lcm(2, 8) == 8

    def test_coprime_numbers(self):
        # LCM of coprimes = their product
        assert lcm(7, 11) == 77

    def test_large_numbers(self):
        # Python handles arbitrary precision natively
        assert lcm(10**18, 10**18 + 1) == (10**18) * (10**18 + 1)


# ─── Integration: HTTP endpoint ──────────────────────────────────────────────

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


URL = "/hesneyhasimaliha_gmail_com"


class TestEndpoint:
    def test_valid_lcm(self, client):
        r = client.get(f"{URL}?x=4&y=6")
        assert r.status_code == 200
        assert r.data == b"12"
        assert r.content_type.startswith("text/plain")

    def test_coprime(self, client):
        r = client.get(f"{URL}?x=7&y=11")
        assert r.data == b"77"

    def test_same_number(self, client):
        r = client.get(f"{URL}?x=5&y=5")
        assert r.data == b"5"

    def test_one_and_n(self, client):
        r = client.get(f"{URL}?x=1&y=100")
        assert r.data == b"100"

    # --- NaN cases ---

    def test_zero_returns_nan(self, client):
        assert client.get(f"{URL}?x=0&y=5").data == b"NaN"
        assert client.get(f"{URL}?x=5&y=0").data == b"NaN"

    def test_negative_returns_nan(self, client):
        assert client.get(f"{URL}?x=-1&y=5").data == b"NaN"

    def test_decimal_returns_nan(self, client):
        assert client.get(f"{URL}?x=1.0&y=5").data == b"NaN"

    def test_string_returns_nan(self, client):
        assert client.get(f"{URL}?x=abc&y=5").data == b"NaN"

    def test_empty_param_returns_nan(self, client):
        assert client.get(f"{URL}?x=&y=5").data == b"NaN"

    def test_missing_param_returns_nan(self, client):
        assert client.get(f"{URL}?x=5").data == b"NaN"
        assert client.get(f"{URL}").data == b"NaN"

    def test_leading_zero_returns_nan(self, client):
        assert client.get(f"{URL}?x=01&y=5").data == b"NaN"

    def test_response_is_plain_text_digits_only(self, client):
        r = client.get(f"{URL}?x=12&y=18")
        assert r.data.decode().isdigit()
