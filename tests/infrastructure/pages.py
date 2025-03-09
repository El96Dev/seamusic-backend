import pytest

from src.infrastructure.pages import get_page, get_has_previous, get_has_next


class TestPagination:
    @pytest.fixture(scope="function")
    def start(self) -> int:
        return 20

    @pytest.fixture(scope="function")
    def size(self) -> int:
        return 10

    @pytest.fixture(scope="function")
    def total(self) -> int:
        return 100

    @pytest.mark.parametrize(
        "size,expected_value",
        [
            (10, 3),
            (3, 7),
            (30, 2),
        ]
    )
    def test_get_page(self, start: int, size: int, expected_value: int) -> None:
        assert get_page(start, size) == expected_value

    @pytest.mark.parametrize(
        "start,expected_value",
        [
            (1, False),
            (2, True),
        ]
    )
    def test_get_has_previous(self, start: int, expected_value: bool) -> None:
        assert get_has_previous(start) is expected_value

    @pytest.mark.parametrize(
        "size,expected_value",
        [
            (200, False),
            (4, True),
        ]
    )
    def test_get_has_next(self, total: int, start: int, size: int, expected_value: bool) -> None:
        assert get_has_next(total, start, size) is expected_value
