import pytest
from src.filters import FilterResult
def test_filter_result_passes_with_no_reasons():
    result = FilterResult(passed=True, reasons=[])
    assert result.passed == True
    assert len(result.reasons) == 0
def test_filter_result_fails_with_reasons():
    result = FilterResult(passed=False, reasons=["Not verified"])
    assert result.passed == False
