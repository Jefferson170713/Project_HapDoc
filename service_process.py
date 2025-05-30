
import pandas as pd

class SearchWindow():
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df_search = pd.DataFrame() 

    