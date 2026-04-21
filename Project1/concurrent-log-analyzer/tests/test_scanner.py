from log_analyzer.scanner import iter_log_files


def test_iter_log_files_finds_log_files_recursively(tmp_path):
    logs_dir = tmp_path / "logs"
    sub_dir = logs_dir / "sub"
    logs_dir.mkdir()
    sub_dir.mkdir()

    file1 = logs_dir / "app1.log"
    file2 = sub_dir / "app2.log"
    file3 = logs_dir / "notes.txt"

    file1.write_text("log1", encoding="utf-8")
    file2.write_text("log2", encoding="utf-8")
    file3.write_text("not a log", encoding="utf-8")

    results = list(iter_log_files(str(logs_dir)))

    result_names = sorted(path.name for path in results)

    assert result_names == ["app1.log", "app2.log"]


def test_iter_log_files_raises_for_missing_directory():
    missing_dir = "this_directory_should_not_exist_123456"
    try:
        list(iter_log_files(missing_dir))
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass