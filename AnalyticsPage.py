import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import plotly.express as px
import seaborn as sns

class AnalyticsPage:
    def __init__(self):
        self.sheet_name = 'SKU & TimeSeries.csv'
        self.df = pd.read_csv(self.sheet_name)
        self.df_sales_single_year = pd.read_csv(self.sheet_name)

    def convert_date_to_day_of_week(self):
        self.df_sales_single_year['Date'] = pd.to_datetime(self.df_sales_single_year['Date'])
        self.df_sales_single_year['Day_of_Week'] = self.df_sales_single_year['Date'].dt.day_name()

    def display_bar_graph_dates(self):
        # Assuming inventory_dataset is your DataFrame
        inventory_dataset = pd.read_csv('Inventory.csv')
        inventory_dataset = inventory_dataset.rename(columns={'Stock in Inventory(In KG for GROCERY)': 'Inventory_Stock'})

        # Sort the DataFrame by 'Inventory_Stock'
        inventory_dataset = inventory_dataset.sort_values(by='Inventory_Stock')

        # Define color conditions
        conditions = [
            (inventory_dataset['Inventory_Stock'] < 100),
            (inventory_dataset['Inventory_Stock'] >= 100) & (inventory_dataset['Inventory_Stock'] <= 180),
            (inventory_dataset['Inventory_Stock'] > 180)
        ]
        inventory_dataset['Name_of_Product'] = np.where((inventory_dataset['SKU_ID'] == 'PER1001'), 'Deodorant',
                            np.where((inventory_dataset['SKU_ID'] == 'PER1002'), 'Toothbrush',
                                     np.where((inventory_dataset['SKU_ID'] == 'PER1003'), 'Lotion',
                                              np.where((inventory_dataset['SKU_ID'] == 'PER1004'), 'Serum',
                                                       np.where((inventory_dataset['SKU_ID'] == 'PER1005'), 'Razor',
                                                                np.where((inventory_dataset['SKU_ID'] == 'PER1006'), 'Hydrator',
                                                                         np.where((inventory_dataset['SKU_ID'] == 'PER1007'), 'Moisturizer',
                                                                                  np.where((inventory_dataset['SKU_ID'] == 'GRO1008'), 'Papad',
                                                                                           np.where((inventory_dataset['SKU_ID'] == 'GRO1009'), 'Ghee',
                                                                                                    np.where((inventory_dataset['SKU_ID'] == 'GRO1010'), 'Paneer',
                                                                                                             np.where((inventory_dataset['SKU_ID'] == 'GRO1011'), 'Moong Dal',
                                                                                                                      np.where((inventory_dataset['SKU_ID'] == 'GRO1012'), 'Basmati Rice',
                                                                                                                               np.where((inventory_dataset['SKU_ID'] == 'GRO1013'), 'Masale',
                                                                                                                                        np.where((inventory_dataset['SKU_ID'] == 'GRO1014'), 'Bread',
                                                                                                                                                 np.where((inventory_dataset['SKU_ID'] == 'HOM1015'), 'Clock',
                                                                                                                                                          np.where((inventory_dataset['SKU_ID'] == 'HOM1016'), 'Blender',
                                                                                                                                                                   np.where((inventory_dataset['SKU_ID'] == 'HOM1017'), 'Bath Towel',
                                                                                                                                                                            np.where((inventory_dataset['SKU_ID'] == 'HOM1018'), 'Pillow',
                                                                                                                                                                                     np.where((inventory_dataset['SKU_ID'] == 'HOM1019'), 'Utensils',
                                                                                                                                                                                              np.where((inventory_dataset['SKU_ID'] == 'HOM1020'), 'Bedsheet',
                                                                                                                                                                                                       'Water Bottle'))))))))))))))))))))
        # Define corresponding hex color codes
        colors = [ '#FF0000','#0000FF', '#008000']

        # Use np.select to apply the conditions and assign colors
        inventory_dataset['bar_color'] = np.select(conditions, colors)

        # Streamlit app
        st.title('Inventory Stock by Product')
        fig = px.bar(inventory_dataset, x='Name_of_Product', y='Inventory_Stock', color_discrete_sequence=inventory_dataset['bar_color'], title='Inventory Stock by Product')

        fig.update_traces(marker_color=inventory_dataset['bar_color'])

        # Sort the bars from lowest to highest
        fig.update_layout(barmode='stack', bargap=0)
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)  # Add borders to bars

        # Show the plot in Streamlit
        st.plotly_chart(fig)

    def display_bar_graph_stock(self):
        # Assuming 'Date' and 'CATEGORY' columns are present in the dataset
        df_sales_single_year = pd.read_csv(self.sheet_name)

        # Convert 'Date' to datetime format
        df_sales_single_year['Date'] = pd.to_datetime(df_sales_single_year['Date'])

        # Group by 'Date' and 'Sub-Category', sum the 'Amount'
        df_plot_sc = df_sales_single_year[['Date', 'CATEGORY', 'Amount']].groupby(['Date', 'CATEGORY']).agg({'Amount': 'sum'}).rename(columns={'Amount': 'Total Sales'}).reset_index()

        # Streamlit app
        st.title(f'Item Sales by Date')

        # Plot the interactive bar chart using Plotly Express with custom styling
        fig = px.bar(df_plot_sc, x='Date', y='Total Sales', color="CATEGORY", title='Item Sales by Date',
                    category_orders={'CATEGORY': ['HOME UTILITIES', 'GROCERY', 'Other']},  # Specify category order
                    labels={'Total Sales': 'Amount'},  # Rename y-axis label
                    color_discrete_map={'HOME UTILITIES': '#1f78b4', 'GROCERY': '#33a02c', 'Other': '#e31a1c'},  # Custom color scheme
                    )
        fig.update_layout(bargap=0.1, bargroupgap=0.1, height=600, width=900, showlegend=True, legend_title_text='Category')
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)  # Add borders to bars

        st.plotly_chart(fig)

    def display_line_graph(self):
        df_time = pd.read_csv('Inventory.csv')  

        df_plot = df_time.groupby('SKU_ID').agg({'Selling Rate': 'mean', 'Buying Rate': 'mean'}).reset_index().sort_values(by='SKU_ID', ascending=True)

        fig = px.line(df_plot, x="SKU_ID", y=["Selling Rate", "Buying Rate"],
                      title='Selling Rate and Buying Rate by SKU_ID')
        st.plotly_chart(fig)

    def display_bar_graph(self):
        self.convert_date_to_day_of_week()

        df_plot_dow = self.df_sales_single_year[['Day_of_Week', 'CATEGORY', 'Amount']].groupby(['Day_of_Week', 'CATEGORY']).agg({'Amount': 'sum'}).rename(columns={'Amount': 'Total Sales'}).reset_index()

        st.title(f'Item Sales by Day of Week')

        fig = px.bar(df_plot_dow, x='Day_of_Week', y='Total Sales', color="CATEGORY", title='Item Sales by Day of Week',
                     category_orders={'Day_of_Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
                     labels={'Total Sales': 'Amount'},
                     color_discrete_map={'HOME UTILITIES': '#1f78b4', 'GROCERY': '#33a02c', 'Other': '#e31a1c'},
                     )
        fig.update_layout(bargap=0.1, bargroupgap=0.1, height=600, width=900, showlegend=True, legend_title_text='Category')
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)
        st.plotly_chart(fig)

    @staticmethod
    def autopct_format(values):
        def autopct_format(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.1f}%'.format(p=pct) if pct > 2 else ''
        return autopct_format

    def display_pie_chart(self):
        dataset = pd.read_csv('SKU & TimeSeries.csv')
        inventory_dataset = pd.read_csv('Inventory.csv')
        df = pd.DataFrame(dataset)
        dataset['Name_of_Product'] = np.where((df['SKU_ID'] == 'PER1001'), 'Deodorant',
                                            np.where((df['SKU_ID'] == 'PER1002'), 'Toothbrush',
                                                        np.where((df['SKU_ID'] == 'PER1003'), 'Lotion',
                                                                np.where((df['SKU_ID'] == 'PER1004'), 'Serum',
                                                                        np.where((df['SKU_ID'] == 'PER1005'), 'Razor',
                                                                                np.where((df['SKU_ID'] == 'PER1006'), 'Hydrator',
                                                                                            np.where((df['SKU_ID'] == 'PER1007'), 'Moisturizer',
                                                                                                    np.where((df['SKU_ID'] == 'GRO1008'), 'Papad',
                                                                                                            np.where((df['SKU_ID'] == 'GRO1009'), 'Ghee',
                                                                                                                    np.where((df['SKU_ID'] == 'GRO1010'), 'Paneer',
                                                                                                                                np.where((df['SKU_ID'] == 'GRO1011'), 'Moong Dal',
                                                                                                                                        np.where((df['SKU_ID'] == 'GRO1012'), 'Basmati Rice',
                                                                                                                                                np.where((df['SKU_ID'] == 'GRO1013'), 'Masale',
                                                                                                                                                        np.where((df['SKU_ID'] == 'GRO1014'), 'Bread',
                                                                                                                                                                    np.where((df['SKU_ID'] == 'HOM1015'), 'Clock',
                                                                                                                                                                            np.where((df['SKU_ID'] == 'HOM1016'), 'Blender',
                                                                                                                                                                                    np.where((df['SKU_ID'] == 'HOM1017'), 'Bath Towel',
                                                                                                                                                                                            np.where((df['SKU_ID'] == 'HOM1018'), 'Pillow',
                                                                                                                                                                                                        np.where((df['SKU_ID'] == 'HOM1019'), 'Utensils',
                                                                                                                                                                                                                np.where((df['SKU_ID'] == 'HOM1020'), 'Bedsheet',
                                                                                                                                                                                                                        'Water Bottle'))))))))))))))))))))
        topcat_subcat = dataset.groupby(['CATEGORY', 'Name_of_Product']).agg({'Amount': 'sum'}).sort_values(
            by="Amount", ascending=False)[:21]
        topcat_subcat = topcat_subcat[["Amount"]].astype(int)
        topcat_subcat = topcat_subcat.sort_values("CATEGORY")
        topcat_subcat.reset_index(inplace=True)
        topcat_subcat_1 = topcat_subcat.groupby(['CATEGORY']).agg({'Amount': 'sum'})
        topcat_subcat_1.reset_index(inplace=True)

        total_revenue = dataset['Amount'].sum()

        plt.rcParams["figure.figsize"] = (36, 36)
        fig, ax = plt.subplots()
        ax.axis('equal')
        width = 0.1
        outer_colors = ['#e57101', '#008062', '#961c2f']
        gradient_colors = ['#ffd1a4', '#febe80', '#feac5c', "#feac5c", "#fe9c3e", "#fe8b1c", '#FE840E',
                        '#9bffe8', '#43ffd3', '#00e9b3', "#00bc91", "#00a680", '#009B77', "#00906f",
                        '#eda1ad', '#e88695', '#e47385', '#e16175', "#da3a53", "#d62944", '#c4253e']
        darkened_colors = []
        for color in gradient_colors:
            rgb_values = mcolors.hex2color(color)
            darkened_rgb = [max(0, value - 0.125) for value in rgb_values]  # Reduce each RGB component by 0.2
            darkened_hex = mcolors.rgb2hex(darkened_rgb)
            darkened_colors.append(darkened_hex)
        inner_colors = darkened_colors
        ax.pie(topcat_subcat_1['Amount'], radius=1, labels=topcat_subcat_1['CATEGORY'], colors=outer_colors,
            wedgeprops=dict(edgecolor='w'), textprops={'fontsize': 30, 'color': 'white', 'weight': 'bold'})
        pie2 = ax.pie(topcat_subcat['Amount'], radius=1 - (width / 2), labels=topcat_subcat['Name_of_Product'],
              autopct=self.autopct_format(topcat_subcat['Amount']), labeldistance=0.7, colors=inner_colors,
              wedgeprops=dict(edgecolor='w'), pctdistance=0.57, rotatelabels=True,
              textprops={'fontsize': 30, 'color': 'white', 'weight': 'bold'})

        fraction_text_list = pie2[2]
        for text in fraction_text_list:
            text.set_rotation(315)
        centre_circle = plt.Circle((0, 0), 0.6, fc='black')  # Set the background color to black
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        ax.annotate('Total Revenue \n ₹' + str(total_revenue), color='white', xy=(0, 0), fontsize=75, ha="center",
                    bbox=dict(boxstyle='round', facecolor='black', edgecolor='none'))  # Set the background color to black

        fig.patch.set_alpha(0.0)  # Set the background color of the entire figure to black

        st.pyplot(fig)

    def run_web_app(self):
        self.display_line_graph()
        self.display_pie_chart()
        self.display_bar_graph()
        self.display_bar_graph_dates()
        self.display_bar_graph_stock()

