EXIT_STATUS=0

echo "Running clippy..."
cargo clippy --manifest-path ../mmr3/Cargo.toml -- -D warnings|| EXIT_STATUS=$?
echo "\n"

echo "Running flake8..."
flake8 ../tests|| EXIT_STATUS=$?
flake8 ../mmr3/python|| EXIT_STATUS=$?
echo "\n"

echo "Running mypy..."
mypy ../tests|| EXIT_STATUS=$?
mypy ../mmr3/python|| EXIT_STATUS=$?
echo "\n"

echo "Exit status code $EXIT_STATUS!" 
exit $EXIT_STATUS
