import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

class AINegotiator:
    def __init__(self):
        self.user = "*User*"
        self.sheet_name = "Initial"

        if 'items' not in st.session_state:
            st.session_state['items'] = ""
        if 'self.sheet_name' not in st.session_state:
            st.session_state['self.sheet_name'] = "Initial"
        if 'quantities' not in st.session_state:
            st.session_state['quantities'] = {}
        if 'selected_wholesaler' not in st.session_state: 
            st.session_state['selected_wholesaler'] = None
        if 'df1' not in st.session_state:
            st.session_state['df1'] = pd.DataFrame()
        if 'df2' not in st.session_state:
            st.session_state['df2'] = pd.DataFrame()

        # Read data from Excel files
        self.item_deals_data = pd.read_excel('item_deals.xlsx')

    def run_web_app(self):
        st.title("AI Negotiator")

        tabs = ["Message Generators", "Negotiator", "Best Deal"]
        selected_tab = st.sidebar.radio("Select Tab:", tabs)

        if selected_tab == "Message Generators":
            self.display_message_generators()
        elif selected_tab == "Negotiator":
            self.display_negotiator()
        elif selected_tab == "Best Deal":
            self.display_best_deal()

    def generate_message_template(self, wholesaler, quantities):
        message = f"Hello from {self.user}!\nI need to restock the following items:\n"

        for item, quantity in quantities.items():
            message += f" - {item} by {quantity} units. Offer: {wholesaler[item + '_offer']}\n"

        message += f"Please tell me the shipping charges and delivery date."
        return message

    def send_message_to_wholesaler(self, wholesaler, quantities):
        reply_message = self.generate_message_template(wholesaler, quantities)
        current_datetime = datetime.now()

        self.wholesaler_data = pd.read_excel('wholesaler_deal.xlsx', self.sheet_name)
        # Update wholesaler details in the Excel file
        # self.wholesaler_data.loc[self.wholesaler_data['wholesaler_name'] == wholesaler['wholesaler_name'],
        #                           ['reply_message', 'shipping_charges', 'delivery_date']] = [
        #     reply_message, 20, current_datetime + timedelta(days=3)
        # ]

        # Save the updated data to the Excel file
        # self.wholesaler_data.to_excel('wholesaler_deal.xlsx', index=False)

    def display_message_generators(self):
        st.header("Message Generators")

        st.session_state['items'] = st.text_area("Enter Item Names (comma-separated):", value=st.session_state.get('items', ""))
        item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))

        st.button("Add Quantity")

        for item in item_list:
            quantity = st.number_input(f"Quantity for {item}:", min_value=1, step=1, format="%d", key=item,
                                       value=st.session_state['quantities'].get(item, 1))
            st.session_state['quantities'][item] = quantity

        if st.button("Generate Template"):
            selected_wholesaler = st.session_state['selected_wholesaler']
            if selected_wholesaler:
                wholesaler = self.wholesaler_data[self.wholesaler_data['wholesaler_name'] == selected_wholesaler].iloc[0]
                template = self.generate_message_template(wholesaler, st.session_state['quantities'])
                st.text_area("Message Template", template, height=200)

        if st.button("Send Message"):
            selected_wholesaler = st.session_state['selected_wholesaler']
            st.session_state['self.sheet_name'] = "Updated"
            st.success("Message sent successfully!")

    def display_negotiator(self):
        st.header("Negotiator")
        map_data = {'LAT': self.wholesaler_data['latitude'].tolist(), 'LON': self.wholesaler_data['longitude'].tolist()}
        st.map(map_data)

        wholesaler_data = pd.read_excel('wholesaler_deal.xlsx', self.sheet_name)

        # Display wholesaler details cards
        for index, wholesaler in wholesaler_data.iterrows():
            with st.expander(f"Wholesaler: {wholesaler['wholesaler_name']}", expanded=True):
                st.write(f"Latitude: {wholesaler['latitude']}")
                st.write(f"Longitude: {wholesaler['longitude']}")
                st.write(f"Reply Message: {wholesaler['reply_message']}")
                st.write(f"Item1 Offer: {wholesaler['item1 offer']}")
                st.write(f"Item2 Offer: {wholesaler['item2 offer']}")
                st.write(f"Item3 Offer: {wholesaler['item3 offer']}")
                st.write(f"Item4 Offer: {wholesaler['item4 offer']}")
                st.write(f"Item5 Offer: {wholesaler['item5 offer']}")
                st.write(f"Shipping Charges: {wholesaler['shipping_charges']}")
                st.write(f"Delivery Date: {wholesaler['delivery_date']}")
        
        st.subheader("Negotiation Details Table")
        st.write(st.session_state['df1'])

        if st.button("Negotiate Deal"):
            # ... (negotiation logic)
            st.success("Deal negotiated successfully!")

   
    def display_best_deal(self):
        st.header("Best Deal")
        map_data = {'LAT': self.wholesaler_data['latitude'].tolist(), 'LON': self.wholesaler_data['longitude'].tolist()}
        st.map(map_data)

        # Display item deals table
        st.subheader("Item Deals Table")
        st.write(self.item_deals_data)

        if st.button("Send Message"):
            # Update item deals table based on user inputs
            for _, item in self.item_deals_data.iterrows():
                for i, wholesaler in self.wholesaler_data.iterrows():
                    item_name = item['item_name']
                    offer = st.text_input(f"Offer for {item_name} from {wholesaler['wholesaler_name']}:",
                                          key=f"{item_name}_{wholesaler['wholesaler_name']}",
                                          value=item[f"{wholesaler['wholesaler_name']}_offer"])
                    self.item_deals_data.at[item.name, f"{wholesaler['wholesaler_name']}_offer"] = offer

            # Save the updated item deals data to the Excel file
            self.item_deals_data.to_excel('item_deals.xlsx', index=False)
            st.success("Item deals updated successfully!")