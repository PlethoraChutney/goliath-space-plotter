import pandas as pd
import plotly.express as px
import sys
from datetime import datetime

# from https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb/63839503
def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

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
    split_paths['Size'] = split_paths['Size'] * 1024
    split_paths["Readable"] = split_paths.Size.apply(humanbytes)

    return(split_paths)

def make_plot(table):
    fig = px.sunburst(
        table,
        path = ['Location', 'Lab', 'User', 'Dir'],
        values = 'Size',
        color = 'User',
        hover_data = ['Readable'],
        title = f'Goliath Usage {datetime.today().strftime("%Y-%m-%d")}'
        )
    fig.write_html('goliath_usage.html')

if __name__ == '__main__':
    table = read_table(sys.argv[1])
    make_plot(table)
