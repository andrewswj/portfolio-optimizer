from collections import OrderedDict
import pandas as pd

# Define an OrderedDict with sample data
data = OrderedDict([('Name', ['Alice', 'Bob', 'Charlie']),
                    ('Age', [25, 30, 35]),
                    ('City', ['New York', 'London', 'Paris'])])

# Convert the OrderedDict to a Pandas DataFrame
df = pd.DataFrame(data)

# Print the resulting DataFrame
print(list(df)[:-1])