EXIT_STATUS=0

echo "Running flake8..."
flake8 ../benchmark|| EXIT_STATUS=$?
echo "\n"

echo "Running mypy..."
mypy ../benchmark|| EXIT_STATUS=$?
echo "\n"

echo "Exit status code $EXIT_STATUS!" 
exit $EXIT_STATUS
