from pathlib import Path
from mentat.treesitter.parser import parse_dir, parse_file


def test_parse_file(temp_testbed):
    test_path = temp_testbed / "multifile_calculator" / "operations.py"
    call_graph = parse_file(test_path, cwd=temp_testbed)
    assert sorted(list(call_graph.nodes.keys())) == sorted(
        [
            "multifile_calculator/operations.py:add_numbers",
            "multifile_calculator/operations.py:multiply_numbers",
            "multifile_calculator/operations.py:subtract_numbers",
            "multifile_calculator/operations.py:divide_numbers",
        ]
    )
    assert dict(call_graph.edges) == {}


def test_parse_dir(temp_testbed):
    test_path = temp_testbed / "multifile_calculator"
    call_graph = parse_dir(test_path, cwd=temp_testbed)
    assert sorted(list(call_graph.nodes.keys())) == sorted(
        [
            "multifile_calculator/operations.py:add_numbers",
            "multifile_calculator/operations.py:multiply_numbers",
            "multifile_calculator/operations.py:subtract_numbers",
            "multifile_calculator/operations.py:divide_numbers",
            "multifile_calculator/calculator.py:calculate",
        ]
    )
    assert call_graph.edges["multifile_calculator/calculator.py:calculate"] == [
        "add_numbers",
        "subtract_numbers",
        "multiply_numbers",
        "divide_numbers",
        "print",
    ]
    assert call_graph.edges["multifile_calculator/calculator.py"] == [
        "fire.Fire",
    ]


def test_call_graph_on_mentat(temp_testbed):
    mentat_path = Path(__file__).parent.parent / "mentat"
    call_graph = parse_dir(mentat_path)
    call_graph.save(temp_testbed / "call_graph.txt")

    saved_call_graph = (temp_testbed / "call_graph.txt").read_text()
    assert saved_call_graph.startswith("NODES\n")
    assert "\nEDGES\n" in saved_call_graph
