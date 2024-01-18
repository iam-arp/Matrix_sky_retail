import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def final_message(input, model="gpt-3.5-turbo", temperature=0):

    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content

# Assumed fixed wholesaler details
WHOLESALE_DATA = pd.DataFrame([
    {
        "wholesaler_name": "Wholesaler A",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler B",
        "latitude": 28.5,
        "longitude": 77.0,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler C",
        "latitude": 28.6,
        "longitude": 77.1,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler D",
        "latitude": 28.7,
        "longitude": 77.2,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler E",
        "latitude": 28.723,
        "longitude": 77.213,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler F",
        "latitude": 28.527,
        "longitude": 77.212,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler G",
        "latitude": 28.7556,
        "longitude": 77.2235,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler H",
        "latitude": 28.72,
        "longitude": 77.21431,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler I",
        "latitude": 28.732,
        "longitude": 77.2,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler J",
        "latitude": 28.7,
        "longitude": 77.2213,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler K",
        "latitude": 28.755,
        "longitude": 77.2,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler L",
        "latitude": 28.7232,
        "longitude": 77.2,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler M",
        "latitude": 28.7,
        "longitude": 77.21,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    },
    {
        "wholesaler_name": "Wholesaler N",
        "latitude": 28.87,
        "longitude": 77.12,
        "reply_message": "",
        "offer": {},
        "shipping_charges": 0,
        "delivery_date": ""
    }
])

class AINegotiator:
    def __init__(self):
        self.user = "Devansh Assawa"

        # if 'responses1' not in st.session_state:
        #     st.session_state['responses1'] = []
        # if 'responses2' not in st.session_state:
        #     st.session_state['responses2'] = []
        if 'items' not in st.session_state:
            st.session_state['items'] = ""
        if 'quantities' not in st.session_state:
            st.session_state['quantities'] = {}
        if 'df1' not in st.session_state:
            st.session_state['df1'] = pd.read_excel('item_deals.xlsx', sheet_name='Initial')
        if 'df2' not in st.session_state:
            st.session_state['df2'] = pd.read_excel('item_deals.xlsx', sheet_name='Updated')

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

    def generate_message_template(self, quantities):
        message = f"Hello from {self.user}!\nI need to restock the following items:\n"

        for item, quantity in quantities.items():
            message += f" - {item} by {quantity} units.\n"

        message += "Please tell me the price and time of the delivery."
        return message

    def display_message_generators(self):
        st.header("Message Generators")

        st.session_state['items'] = st.text_area("Enter Item Names (comma-separated):", value=st.session_state['items'])
        item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))

        st.button("Add Quantity")

        for item in item_list:
            quantity = st.number_input(f"Quantity for {item}:", min_value=1, step=1, format="%d", key=item,
                                       value=st.session_state['quantities'].get(item, 1))
            st.session_state['quantities'][item] = quantity

        if st.button("Generate Template"):
            template = self.generate_message_template(st.session_state['quantities'])
            messages_6 =  [
            {'role':'system',
            'content':"""You are an AI negotiator representing Mr. Assawa, a grocery store owner. Your task is to compose a message for wholesalers, inquiring about the prices of specified items and their quantities. You will receive input containing details and a list of items that we need to purchase."""},
            {'role':'user',
            'content':f""" {template}."""},
            ]
            response2 = final_message(messages_6, temperature=1)
            st.text_area("Message Template", response2, height=200)

        if st.button("Send Message"):
            # item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))
            # for i, item in enumerate(item_list, start=1):
            #     st.session_state['responses1'].append({
            #         "wholesaler_name": f"Wholesaler {i}",
            #         "message": f"Example Message for {item}",
            #         "price": 100 + i * 10,
            #         "shipping_charges": 10 + i * 2,
            #         "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            #         "latitude": 28.6278 + i * 0.1,  # Adjust the latitude for each wholesaler
            #         "longitude": 77.2190 + i * 0.1  # Adjust the longitude for each wholesaler
            #     })
            st.session_state['df1'] = pd.read_excel('item_deals.xlsx', sheet_name='Updated')
            st.success("Message sent successfully!")

    def display_negotiator(self):
        st.header("Negotiator")
        map_data = {'LAT': WHOLESALE_DATA['latitude'].tolist(), 'LON': WHOLESALE_DATA['longitude'].tolist()}
        st.map(map_data)

        wholesaler_data = pd.read_excel('wholesaler_deal.xlsx', sheet_name='Initial')

        num_rows_to_display = 4
        display_data = wholesaler_data.head(num_rows_to_display)

        # Display the initial rows
        for index, wholesaler in display_data.iterrows():
            with st.expander(f"Wholesaler: {wholesaler['wholesaler_name']}", expanded=True):
                st.write(f"Reply Message: {wholesaler['reply_message']}")
                st.write(f"Rice: ₹{wholesaler['item1_offer']}")
                st.write(f"Wheat: ₹{wholesaler['item2_offer']}")
                st.write(f"Refined Oil: ₹{wholesaler['item3_offer']}")
                st.write(f"Sugar: ₹{wholesaler['item4_offer']}")
                st.write(f"Daal: ₹{wholesaler['item5_offer']}")
                st.write(f"Shipping Charges: ₹{wholesaler['shipping_charges']}")
                st.write(f"Total Charges: ₹{wholesaler['total_cost']}")
                st.write(f"Delivery Time: {wholesaler['delivery_date']}")

        # Add a button to load more rows
        if st.button("Load More"):
            # Display the remaining rows
            remaining_data = wholesaler_data.iloc[num_rows_to_display:]
            for index, wholesaler in remaining_data.iterrows():
                with st.expander(f"Wholesaler: {wholesaler['wholesaler_name']}", expanded=True):
                    st.write(f"Reply Message: {wholesaler['reply_message']}")
                    st.write(f"Rice: ₹{wholesaler['item1_offer']}")
                    st.write(f"Wheat: ₹{wholesaler['item2_offer']}")
                    st.write(f"Refined Oil: ₹{wholesaler['item3_offer']}")
                    st.write(f"Sugar: ₹{wholesaler['item4_offer']}")
                    st.write(f"Daal: ₹{wholesaler['item5_offer']}")
                    st.write(f"Shipping Charges: ₹{wholesaler['shipping_charges']}")
                    st.write(f"Total Charges: ₹{wholesaler['total_cost']}")
                    st.write(f"Delivery Time: {wholesaler['delivery_date']}")


        st.subheader("Negotiation Details Table")
        st.write(st.session_state['df1'])
        if st.button("Negotiate Deal"):
            # item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))
            # for i, item in enumerate(item_list, start=1):
            #     st.session_state['responses2'].append({
            #         "wholesaler_name": f"Wholesaler {i}",
            #         "message": f"Example Message for {item}",
            #         "price": 100 + i * 10,
            #         "shipping_charges": 10 + i * 2,
            #         "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            #         "latitude": 28.6278 + i * 0.1,  # Adjust the latitude for each wholesaler
            #         "longitude": 77.2190 + i * 0.1  # Adjust the longitude for each wholesaler
            #     })
            #     map_data['LAT'].append(response['latitude'])
            #     map_data['LON'].append(response['longitude'])
            # st.session_state['df2'] = pd.read_excel('best deal table.xlsx')
            st.session_state['df2'] = pd.read_excel('item_deals.xlsx', sheet_name='Updated')
            st.success("Deal negotiated successfully!")

    def display_best_deal(self):
        st.header("Best Deal")
        map_data = {'LAT': WHOLESALE_DATA['latitude'].tolist(), 'LON': WHOLESALE_DATA['longitude'].tolist()}
        st.map(map_data)
        wholesaler_data = pd.read_excel('wholesaler_deal.xlsx', sheet_name='Updated')

        num_rows_to_display = 4
        display_data = wholesaler_data.head(num_rows_to_display)

        # Display the initial rows
        for index, wholesaler in display_data.iterrows():
            with st.expander(f"Wholesaler: {wholesaler['wholesaler_name']}", expanded=True):
                st.write(f"Reply Message: {wholesaler['reply_message']}")
                st.write(f"Rice (initial offer): ₹{wholesaler['item1_offer']}")
                st.write(f"Rice (finaloffer): ₹{wholesaler['item1_final']}")
                st.write(f"Wheat (initial offer): ₹{wholesaler['item2_offer']}")
                st.write(f"Wheat (finaloffer): ₹{wholesaler['item2_final']}")
                st.write(f"Refined Oil (initial offer): ₹{wholesaler['item3_offer']}")
                st.write(f"Refined Oil (finaloffer): ₹{wholesaler['item3_final']}")
                st.write(f"Sugar (initial offer): ₹{wholesaler['item4_offer']}")
                st.write(f"Sugar (finaloffer): ₹{wholesaler['item4_final']}")
                st.write(f"Daal (initial offer): ₹{wholesaler['item5_offer']}")
                st.write(f"Daal (finaloffer): ₹{wholesaler['item5_final']}")
                st.write(f"Shipping Charges: ₹{wholesaler['shipping_charges']}")
                st.write(f"Total Charges: ₹{wholesaler['total_cost']}")
                st.write(f"Total Savings: ₹{wholesaler['cost_saved']}")
                st.write(f"Delivery Time: {wholesaler['delivery_date']}")

        # Add a button to load more rows
        if st.button("Load More"):
            # Display the remaining rows
            remaining_data = wholesaler_data.iloc[num_rows_to_display:]
            for index, wholesaler in remaining_data.iterrows():
                with st.expander(f"Wholesaler: {wholesaler['wholesaler_name']}", expanded=True):
                    st.write(f"Latitude: {wholesaler['latitude']}")
                    st.write(f"Longitude: {wholesaler['longitude']}")
                    st.write(f"Reply Message: {wholesaler['reply_message']}")
                    st.write(f"Item1 Offer: {wholesaler['item1_offer']}")
                    st.write(f"Item2 Offer: {wholesaler['item2_offer']}")
                    st.write(f"Item3 Offer: {wholesaler['item3_offer']}")
                    st.write(f"Item4 Offer: {wholesaler['item4_offer']}")
                    st.write(f"Item5 Offer: {wholesaler['item5_offer']}")
                    st.write(f"Shipping Charges: {wholesaler['shipping_charges']}")
                    st.write(f"Delivery Date: {wholesaler['delivery_date']}")
        st.subheader("Best Deal Table")
        st.write(st.session_state['df2'])

        if st.button("Place Order"):
            # Your logic to fill the "Best Deal" entries with respective values
            st.success("Order placed successfully!")
