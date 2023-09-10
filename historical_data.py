import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class  Get_Historical_Data:
    
    
    def __init__(self, symbols, exchange, initial_date, last_date, api_key):
        
        ### Attributes
        self.ENDPOINT = "http://api.marketstack.com/v1/eod"
        self.API_KEY = api_key
        self.symbols = symbols
        self.exchange = exchange
        self.initial_date = initial_date
        self.last_date = last_date
        self.limit = 1000
        self.offset = 0
        
        # Params dict
        self.params = {
            'access_key': self.API_KEY,
            'symbols': self.symbols,
            'exchange': self.exchange,
            'date_from': self.initial_date,
            'date_to': self.last_date,
            'limit': self.limit,
            'offset': self.offset,
            'sort': 'ASC'
        }
        
        self.all_data = []
    
    ### Methods: 
    
    def historical_data(self):
        
        while True:
            response = requests.get(self.ENDPOINT, params=self.params)
    
            if response.status_code == 200:
                data = response.json()['data']
                self.all_data.extend(data)
        
                if len(data) < self.params['limit']:
                    break
        
        
                self.params['offset'] += self.params['limit']
        
            else:
                print(f"Error {response.status_code}: {response.text}")
                break
        # Creating the df    
        self.df = pd.DataFrame(self.all_data)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['date'] = self.df['date'].dt.date
            
        return self.df
    
    def get_plot(self):
        plt.figure(figsize=(14,7))
        plt.plot(self.df['date'], self.df['close'], label='Close Price')
        plt.title(f"Close Price of {self.params['symbols']} from {self.df['date'].min()} to {self.df['date'].max()}")
        plt.xlabel('Date')
        plt.ylabel('Close Price USD')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        
    def get_plot_2(self):
        # mean, min and max values
        maximo = self.df['close'].max()
        minimo = self.df['close'].min()
        medio = self.df['close'].mean()
        
        # Crear Gráfico
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=self.df['date'], y=self.df['close'], mode='lines+markers', name='Close Price'))
        
        fig.add_trace(
            go.Scatter(
                x=[self.df['date'].min(), self.df['date'].max()],
                y=[maximo, maximo],
                mode='lines',
                line=dict(color='Red', width=1, dash='dashdot'),
                name=f'Máximo: {maximo}'
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=[self.df['date'].min(), self.df['date'].max()],
                y=[minimo, minimo],
                mode='lines',
                line=dict(color='Green', width=1, dash='dashdot'),
                name=f'Mínimo: {minimo}'
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=[self.df['date'].min(), self.df['date'].max()],
                y=[medio, medio],
                mode='lines',
                line=dict(color='Blue', width=1, dash='dashdot'),
                name=f'Medio: {medio}'
            )
        )
        
        fig.update_layout(autosize = False, width = 1700, height = 600)
        
        fig.show()    