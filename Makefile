check: type_check test_check# run all check

type_check: # run all type check
	uv run ty check

test_check: # run all test check
	uv run pytest

green: # run green git gamble command
	git-gamble --green -m "green" -- make check

red: # run red git gamble command 
	git-gamble --red -m "red" -- make check
