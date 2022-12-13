import matplotlib.pyplot as plt
import seaborn as sns

def plot_graph(dataframe):

    #dados_plot = dataframe.query('Gender == @categoria')

    fig, ax = plt.subplots(figsize=(8,6))
    ax = sns.barplot(x = 'Months_on_book', y = 'Credit_Limit', data = dataframe)
    ax.set_title(f'Meses de relacionamento com o banco X Limite de crédito', fontsize = 14)
    ax.set_xlabel('Limite de crédito', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Meses de relacionamento com o banco', fontsize = 12)
  
    return fig
