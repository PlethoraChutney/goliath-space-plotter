import pandas as pd
import plotly.express as px
import sys
from datetime import datetime

def humanbytes(B):
   prefixes = ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

   prefix_index = 0
   while B >= 1024 and prefix_index+1 < len(prefixes):
      B = B/1024
      prefix_index += 1

   return f"{B:.1f} {prefixes[prefix_index]}B"

def read_table(filename):
    table = pd.read_table(
        filename,
        sep = '\t',
        header = 0,
        names = ['Size', 'Path']
    )

    split_paths = table.Path.str.split(pat = '/', expand = True).drop(columns = [0,1])
    split_paths.columns = ['Location', 'Lab', 'User', 'Dir']
    split_paths['Size'] = table['Size']
    split_paths = split_paths[split_paths.Dir.notnull()]
    # Multiply by 1024 b/c du output default is kB
    split_paths["Readable"] = split_paths.Size.apply(lambda x: humanbytes(x * 1024))
    # Then conver to TB for ease of reading
    split_paths['Size'] = split_paths['Size'] / 1024**3

    return(split_paths)

def make_plot(table):
    total = sum(table['Size'])

    fig = px.sunburst(
        table,
        path = ['Location', 'Lab', 'User', 'Dir'],
        values = 'Size',
        color = 'User',
        hover_data = ['Readable'],
        title = f'Goliath Usage {datetime.today().strftime("%Y-%m-%d")}; Size: {humanbytes(total * 1024**4)}'
        )
    fig.write_html('goliath_usage.html')

if __name__ == '__main__':
    table = read_table(sys.argv[1])
    table.to_csv('goliath-du.csv')
    make_plot(table)
