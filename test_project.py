from project import calculate_configuration, total_electrons, get_shell_label


def test_calculate_configuration():
    assert calculate_configuration(1) == [1]
    assert calculate_configuration(10) == [2, 8]
    assert calculate_configuration(18) == [2, 8, 8]


def test_total_electrons():
    assert total_electrons([2, 8]) == 10
    assert total_electrons([2, 8, 8]) == 18


def test_get_shell_label():
    assert get_shell_label(0) == "K"
    assert get_shell_label(1) == "L"
    assert get_shell_label(2) == "M"
