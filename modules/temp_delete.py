import pandas as pd

d=pd.read_excel('Sanity_Test.xlsx',sheet_name='Test_Cases')
#self.df = pd.read_excel('Sanity_Test.xlsx', 'Test_Cases', index_col=None)
print(d)