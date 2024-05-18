import pandas as pd
from bs4 import BeautifulSoup
from scrape_wiki import scrape_table

# Create a sample table for testing
html = """
<table>
    <tbody>
        <tr>
            <td>Polish Name 1</td>
            <td>Latin Name 1</td>
        </tr>
        <tr>
            <td>Polish Name 2</td>
            <td>Latin Name 2</td>
        </tr>
    </tbody>
</table>
"""
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

# Call the function
result = scrape_table(table)

# Create the expected output
expected_output = pd.DataFrame({
    "Polish Name": ["Polish Name 1", "Polish Name 2"],
    "Latin Name": ["Latin Name 1", "Latin Name 2"]
})

# Use the assert statement to check if the function returns the expected output
assert result.equals(expected_output), "Test failed: The function did not return the expected output."

print("Test passed: The function returned the expected output.")