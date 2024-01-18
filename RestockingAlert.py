import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def final_message(input, model="gpt-3.5-turbo", temperature=0):

    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content

class RestockingAlert:

    # def fetch_data_from_excel(self, SKU_ID, analytics_df):
    #     # Filter the dataframe based on SKU_ID
    #     item_data = analytics_df[analytics_df['SKU_ID'] == SKU_ID]
        
    #     # Extract selling rate and current stock (quantity)
    #     selling_rate = item_data['Selling Rate'].values[0]
    #     current_stock = item_data['Stock in Inventory(In KG for GROCERY)'].values[0]

    #     return selling_rate, current_stock

    @staticmethod
    def calculate_time_to_last(selling_rate, current_stock):
        if selling_rate > 0:
            time_to_last = current_stock / selling_rate
        else:
            time_to_last = float('inf')
        return time_to_last

    def run_web_app(self):
        st.title("Inventory Management System - Restocking Alert")
        st.divider()
        st.subheader("The following stocks need urgent restocking as they will last for less than 15 days")

        # Read data from analytics.xlsx
        analytics_df = pd.read_excel("analytics.xlsx")

        first_5_items = analytics_df.head(5)
        
        for index, row in first_5_items.iterrows():
            name = row['Product Name']
            days = row['Days left']
            insight = row['Insights']
            
            # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
            messages =  [
            {'role':'system',
            'content':"""You are an assistant at Assawa Store, specializing in efficient inventory management. Your responsibility includes issuing alerts for items requiring restocking and estimating the remaining days before they run out of stock, and insights overview. Input provides item name along with the corresponding number of days until depletion and one insights"""},
            {'role':'user',
            'content':f"""{name}, {days}, {insight}"""},
            ]
            response = final_message(messages, temperature=1)
            # print(response)
            st.warning(response)
            
        # Adding "Show More" button
        if st.button("Show More"):
            # Fetching and displaying remaining items
            remaining_items = analytics_df.iloc[5:]
            
            for index, row in remaining_items.iterrows():
                name = row['Product Name']
                days = row['Days left']
                insight = row['Insights']
                
                # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
                messages =  [
                {'role':'system',
                'content':"""You are an assistant at Assawa Store, specializing in efficient inventory management. Your responsibility includes issuing alerts for items requiring restocking and estimating the remaining days before they run out of stock, and insights overview. Input provides item name along with the corresponding number of days until depletion and one insights"""},
                {'role':'user',
                'content':f"""{name}, {days}, {insight}"""},
                ]
                response = final_message(messages, temperature=1)
                # print(response)
                st.warning(response)

        # Plotting selling rates and buying rates
        # fig, ax = self.plot_rates(analytics_df)
        # st.pyplot(fig)

    def get_sku_units_needing_restock(self, analytics_df):
        items_needing_restock = []

        for SKU_ID in analytics_df['SKU_ID']:
            selling_rate, current_stock = self.fetch_data_from_excel(SKU_ID, analytics_df)
            time_to_last = self.calculate_time_to_last(selling_rate, current_stock)

            if time_to_last < 5:
                items_needing_restock.append(SKU_ID)

        return items_needing_restock

    @staticmethod
    def plot_rates(analytics_df):
        # Plotting selling rates and buying rates
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(analytics_df['SKU_ID'], analytics_df['Selling Rate'], label='Selling Rate', marker='o')
        ax.plot(analytics_df['SKU_ID'], analytics_df['Buying Rate'], label='Buying Rate', marker='o')

        ax.set_title('Selling and Buying Rates Over SKU Units')
        ax.set_xlabel('SKU Unit')
        ax.set_ylabel('Rate')
        ax.legend()
        ax.grid(True)

        return fig, ax
