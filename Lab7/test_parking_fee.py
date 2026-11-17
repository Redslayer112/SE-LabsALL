import re
from hypothesis import given, strategies as st
from parking_fee import minutes_parked, hourly_rate, format_plate

@given(st.text() | st.none())
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e}"

@given(st.text() | st.none())
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed with: {e}"

@given(st.text() | st.none())
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed with: {e}"

@given(st.integers(0, 99), st.integers(0, 99), st.integers(0, 99), st.integers(0, 99))
def test_minutes_parked_range(h1, m1, h2, m2):
    result = minutes_parked(f"{h1:02}:{m1:02}-{h2:02}:{m2:02}")
    assert result is None or 0 <= result < 24 * 60

@given(st.text(alphabet="ka01AB234 ", max_size=12))
def test_format_plate_shape(s):
    result = format_plate(s)
    assert result is None or re.fullmatch(r"[A-Z]{2} [0-9]{2} [A-Z]{2} [0-9]{4}", result)
