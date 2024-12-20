import streamlit as st
import pandas as pd
import altair as alt


st.title("Restaurant Dashboard")
st.write("This interactive dashboard for restaurant manager to track employee performance and operational efficiency.")
# let user upload file 
uploaded_file = st.file_uploader("Please upload CSV file.", type=['csv'])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # convert to datetime 
    data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    data['Order Time'] = pd.to_datetime(data['Order Time'])
    data['Serve Time'] = pd.to_datetime(data['Serve Time'])
    # calculate waiting order time
    data['Waiting_Time'] = data['Serve Time'] - data['Order Time']
    # convert waiting time to int
    data['Waiting_Time'] = data['Waiting_Time'].dt.total_seconds() / 60
    data['Waiting_Time'] = data['Waiting_Time'].astype(int)
    # covert datetime to month
    data['Month'] = data['Order Time'].dt.to_period('M').dt.strftime('%m-%Y')
    st.write("Overall Data")
    st.write(data.head())

    # -------------------------------------------------------------------------------- 
    # -------------------------------------------------------------------------------- 
    # overall monthly sale by category
    st.write("## Dashboard 1: Overall Sales and Total Sales.")
    # count order and group data by category and month
    overall_sales_category = data.groupby(['Month', 'Category']).agg(
        Order_Count=('Price', 'count'),
        Sales=('Price', 'sum')).reset_index()

    # create tab to store 2 chart display when user click on tab
    tabA, tabB = st.tabs(['Sales Order', 'Total Sale']) 
    with tabA:
        # dashboard display overall sale by category using altair chart : https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart
        overall_sales_chart = (
            alt.Chart(overall_sales_category)
            .mark_line(point=True)
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Order_Count:Q', title='Number of Order'),
                color='Category:N',
                tooltip=['Month', 'Category', 'Order_Count']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Overall Sales Trend by Category")
        st.write("") # add space between titel and chart
        st.altair_chart(overall_sales_chart)
    with tabB:
        # dashboard for overall total sales in month by category
        overall_total_sales_chart = (
            alt.Chart(overall_sales_category)
            .mark_line(point=True)
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Sales:Q'),
                color='Category:N',
                tooltip=['Month', 'Category', 'Sales']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Overall Total Sales Trend by Category")
        st.write("") # add space between titel and chart
        st.altair_chart(overall_total_sales_chart)
    

    # -------------------------------------------------------------------------------- 
    # -------------------------------------------------------------------------------- 
    # overall monthly sale by menu
    st.write("## Dashboard 2: Best and Lowest Seller Menu")
    # count order and group data by menu and month
    menu_sales = data.groupby(['Month', 'Menu', 'Category']).size().reset_index(name='Order_Count')
    # filter best seller menu for drink and food
    drink_menu = menu_sales[menu_sales['Category'] == 'drink']
    food_menu = menu_sales[menu_sales['Category'] == 'food']
    # find best seller menu for each month
    best_drink_menu = drink_menu.loc[drink_menu.groupby('Month')['Order_Count'].idxmax()]
    best_food_menu = food_menu.loc[food_menu.groupby('Month')['Order_Count'].idxmax()]
    # find lowest seller menu for each month
    low_drink_menu = drink_menu.loc[drink_menu.groupby('Month')['Order_Count'].idxmin()]
    low_food_menu = food_menu.loc[food_menu.groupby('Month')['Order_Count'].idxmin()]


    # create tab to store 2 chart display when user click on tab
    tab1, tab2 = st.tabs(["Best Seller", "Lowest Seller"])


    # create bar chart to display best seller menu in each month
    with tab1:
        best_drink_chart = (
            alt.Chart(best_drink_menu)
            .mark_bar()
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Order_Count:Q', title='Number of Order'),
                color=alt.Color('Menu:N'),
                tooltip=['Month', 'Menu', 'Order_Count']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Best Seller Drink Menu by Month")
        st.write("") # add space between titel and chart
        st.altair_chart(best_drink_chart)

        best_food_chart = (
            alt.Chart(best_food_menu)
            .mark_bar()
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Order_Count:Q', title='Number of Order'),
                color=alt.Color('Menu:N'),
                tooltip=['Month', 'Menu', 'Order_Count']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Best Seller Food Menu by Month")
        st.write("") # add space between titel and chart
        st.altair_chart(best_food_chart)
    # -------------------------------------------------------------------------------- 
    # create bar chart to display bad seller menu in each month
    with tab2:
        low_drink_chart = (
            alt.Chart(low_drink_menu)
            .mark_bar()
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Order_Count:Q', title='Number of Order'),
                color=alt.Color('Menu:N'), 
                tooltip=['Month', 'Menu', 'Order_Count']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Lowest Seller Drink Menu by Month")
        st.write("") # add space between titel and chart
        st.altair_chart(low_drink_chart)

        low_food_chart = (
            alt.Chart(low_food_menu)
            .mark_bar()
            .encode(
                x=alt.X('Month:N', sort=None),
                y=alt.Y('Order_Count:Q', title='Number of Order'),
                color=alt.Color('Menu:N'), 
                tooltip=['Month', 'Menu', 'Order_Count']
            )
            .properties(
                width=700,
                height=400
            )
        )
        st.write("#### Lowest Seller Food Menu by Month")
        st.write("") # add space between titel and chart
        st.altair_chart(low_food_chart)
        


    # -------------------------------------------------------------------------------- 
    # -------------------------------------------------------------------------------- 
    # overall avg waiting time vs avg staff 
    st.write("## Dashboard 3: Overall Waiting Time Vs Number of Staff.")
    # fillter category data and then group data to display on dashboard
    drink_data = data[data['Category'] == 'drink']
    drink_summary = drink_data.groupby('Month').agg(
        Avg_Waiting_Time=('Waiting_Time', 'mean'),
        Avg_Drink_Staff=('Drinks Staff', 'mean'),
        Order_Count=('Waiting_Time', 'count')).reset_index()
    food_data = data[data['Category'] == 'food']
    food_summary = food_data.groupby('Month').agg(
        Avg_Waiting_Time=('Waiting_Time', 'mean'),
        Avg_Kitchen_Staff=('Kitchen Staff', 'mean'),
        Order_Count=('Waiting_Time', 'count')).reset_index()
    # create tab to store 2 chart display when user click on tab
    tab3, tab4 = st.tabs(['Drink', 'Food'])

    with tab3:
        drink_chart = (
            alt.Chart(drink_summary)
            .mark_bar(color='steelblue')
            .encode(
                x=alt.X('Month:N', title='Month'),
                y=alt.Y('Avg_Drink_Staff:Q', title='Number of Staff'),
                tooltip=['Month', 'Avg_Waiting_Time', 'Avg_Drink_Staff', 'Order_Count']
            )
        ) + (
            alt.Chart(drink_summary)
            .mark_line(color='orange', point=True)
            .encode(
                x=alt.X('Month:N'),
                y=alt.Y('Avg_Waiting_Time:Q', title='Waiting Time (minutes)'),
                tooltip=['Month', 'Avg_Waiting_Time', 'Order_Count','Avg_Drink_Staff']
            )
            .properties(
                width=700,
                height=400
            )
        ) 
        # + (
        #     alt.Chart(drink_summary)
        #     .mark_line(color='pink', point=True)
        #     .encode(
        #         x=alt.X('Month:N'),
        #         y=alt.Y('Avg_Drink_Staff:Q', title='Avg_Drink_Staff'),
        #         tooltip=['Month', 'Avg_Waiting_Time', 'Order_Count','Avg_Drink_Staff']
        #     )
        #     .properties(
        #         width=700,
        #         height=400
        #     )
        # )
        st.write("#### Overall Waiting Time with Number of Staff for Drink Menu")
        st.write("""
                    - **Steel Blue (Bar)**: Average Staff Count
                    - **Orange (Line)**: Average Waiting Time (minutes)
                """)
        st.write("") # add space between titel and chart
        st.altair_chart(drink_chart)
    # -------------------------------------------------------------------------------- 
    with tab4:
        food_chart = (
            alt.Chart(food_summary)
            .mark_bar(color='steelblue')
            .encode(
                x=alt.X('Month:N', title='Month'),
                y=alt.Y('Avg_Kitchen_Staff:Q', title='Number of Staff'),
                tooltip=['Month', 'Avg_Waiting_Time', 'Avg_Kitchen_Staff', 'Order_Count']
            )
        ) + (
            alt.Chart(food_summary)
            .mark_line(color='orange', point=True)
            .encode(
                x=alt.X('Month:N'),
                y=alt.Y('Avg_Waiting_Time:Q', title='Waiting Time (minutes)'),
                tooltip=['Month', 'Avg_Waiting_Time', 'Order_Count','Avg_Kitchen_Staff']
            )
            .properties(
                width=700,
                height=400)
        ) 
        # + (
        #     alt.Chart(food_summary)
        #     .mark_line(color='pink', point=True)
        #     .encode(
        #         x=alt.X('Month:N'),
        #         y=alt.Y('Avg_Kitchen_Staff:Q'),
        #         tooltip=['Month', 'Avg_Waiting_Time', 'Order_Count','Avg_Kitchen_Staff']
        #     )
        #     .properties(
        #         width=700,
        #         height=400
        #     )
        # )
        st.write("#### Overall Waiting Time with Number of Staff for Food Menu")
        st.write(""" 
                    - **Steel Blue (Bar)**: Average Staff Count
                    - **Orange (Line)**: Average Waiting Time (minutes)
                """)
        st.write("") # add space between titel and chart
        st.altair_chart(food_chart)


    # -------------------------------------------------------------------------------- 
    # -------------------------------------------------------------------------------- 
    st.write("## Dashboard 4: Monthly overview of Average Waiting time, Staff count and Orders by Date")
    st.write("#### This chart shown the relationships between average waiting order time with number of staffs and orders by date.")
    st.write("Please Select Month to see chart")
    # create selection for user
    select_month = st.selectbox("Select a Month", options=data['Month'].unique())
    # filter data to display on dashboard
    filter_data = data[data['Month'] == select_month]
    # group to drink and food data
    drink_data_month = filter_data[filter_data['Category'] == 'drink'].groupby('Date').agg(
        Avg_Waiting_Time = ('Waiting_Time', 'mean'),
        Drink_Staff = ('Drinks Staff', 'mean'),
        Order_Count=('Waiting_Time', 'count')).reset_index()
    food_data_month = filter_data[filter_data['Category'] == 'food'].groupby('Date').agg(
        Avg_Waiting_Time = ('Waiting_Time', 'mean'),
        Kitchen_Staff = ('Kitchen Staff', 'mean'),
        Order_Count=('Waiting_Time', 'count')).reset_index()
    # create tab to store 2 chart display when user click on tab
    tab5, tab6 = st.tabs(['Drink','Food'])

    if not filter_data.empty:
        with tab5:
            drink_chart = (
                alt.Chart(drink_data_month)
                .mark_bar(color='steelblue')
                .encode(
                    x=alt.X('Date:N', title='Date'),
                    y=alt.Y('Order_Count:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Drink_Staff', 'Order_Count']
                )
            ) + (
                alt.Chart(drink_data_month)
                .mark_line(color='orange', point=True)
                .encode(
                    x=alt.X('Date:N'),
                    y=alt.Y('Avg_Waiting_Time:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Order_Count','Drink_Staff']
                )
                .properties(
                    width=700,
                    height=400
                )
            ) + (
                alt.Chart(drink_data_month)
                .mark_line(color='pink', point=True)
                .encode(
                    x=alt.X('Date:N'),
                    y=alt.Y('Drink_Staff:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Order_Count','Drink_Staff']
                )
                .properties(
                    width=700,
                    height=400
                )
            )
            st.write("#### Waiting Time, Staff Count and Orders for Drink Category")
            st.write("""
                     - **Steel Blue (Bar)**: Total Orders
                     - **Orange (Line)**: Average Waiting Time (minutes)
                     - **Pink (Dashed Line)**: Average Staff Count
                    """)
            st.write("") # add space between titel and chart 
            st.altair_chart(drink_chart)
        # -------------------------------------------------------------------------------- 
        with tab6:
            food_chart = (
                alt.Chart(food_data_month)
                .mark_bar(color='steelblue')
                .encode(
                    x=alt.X('Date:N', title='Date'),
                    y=alt.Y('Order_Count:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Kitchen_Staff', 'Order_Count']
                )
            ) + (
                alt.Chart(food_data_month)
                .mark_line(color='orange', point=True)
                .encode(
                    x=alt.X('Date:N'),
                    y=alt.Y('Avg_Waiting_Time:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Order_Count']
                )
                .properties(
                    width=700,
                    height=400
                )
            ) + (
                alt.Chart(food_data_month)
                .mark_line(color='pink', point=True)
                .encode(
                    x=alt.X('Date:N'),
                    y=alt.Y('Kitchen_Staff:Q'),
                    tooltip=['Date', 'Avg_Waiting_Time', 'Order_Count','Kitchen_Staff']
                )
                .properties(
                    width=700,
                    height=400
                )
            )
            st.write("#### Waiting Time, Staff Count and Orders for Food Category")
            st.markdown("""
                     - **Steel Blue (Bar)**: Total Orders
                     - **Orange (Line)**: Average Waiting Time (minutes)
                     - **Pink (Dashed Line)**: Average Staff Count
                    """)
            st.write("") # add space between titel and chart
            st.altair_chart(food_chart)
    else:
        st.warning("No data available for the selected month")

    
    # -------------------------------------------------------------------------------- 
    # -------------------------------------------------------------------------------- 
    st.write("### Dashboard 5: Orders by Time of Day")
    # group data by hour and count the number of orders
    orders_by_hour = data.groupby('Hour').size().reset_index(name='Order_Count')

    # create bar chart to show order count by hour
    order_time_chart = (
        alt.Chart(orders_by_hour)
        .mark_bar(color='steelblue')
        .encode(
            x=alt.X('Hour:O', title='Hour of the Day'), # , axis=alt.Axis(format='02d')
            y=alt.Y('Order_Count:Q', title='Number of Orders'),
            tooltip=['Hour', 'Order_Count']
        )
        .properties(
            width=700,
            height=400,
        )
    )
    # st.write("#### Order Distribution by Hour")
    # st.markdown("""
    # - This chart shows the distribution of orders throughout the day.
    # - Use it to identify peak times and plan staffing or inventory accordingly.
    # """)
    st.write("") # add space between titel and chart 
    st.altair_chart(order_time_chart)

    # create peak order time 
    peak_hour = orders_by_hour.loc[orders_by_hour['Order_Count'].idxmax()]
    st.write(f"**Peak Order Time:** {peak_hour['Hour']:02d}:00 with {peak_hour['Order_Count']} orders.")






