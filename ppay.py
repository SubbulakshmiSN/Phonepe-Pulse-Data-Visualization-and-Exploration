
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from streamlit_option_menu import option_menu

#creating connection to SQL
p_db= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="1234",
                        database="phonepe_pulse_data",
                        port="5432")
cursor= p_db.cursor()

#page navigation
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                  )


#sidebar option set up
with st.sidebar:
    st.caption(":violet[*Application created by Subbulakshmi*]")
    select_page= option_menu("Phonepe Pulse",["Home", "Explore Data", "Insights"],
                  icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                  menu_icon= "menu-button-wide",
                  default_index=0,
                  styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

#setting up home page
if select_page == "Home":

    col1,col2= st.columns(2)
    
    with col1:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("##")
        st.markdown("######")
        st.write("------")
        st.markdown(":blue[*PhonePe is an Indian digital payments and financial technology company*]")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        

                
    with col2:
        st.title(":blue[Phonepe Pulse Data visualization with plotly]")
        st.write(":violet[Technologies used :] Github Cloning, Python, Pandas, PostgreSQL, Streamlit, and Plotly.")
        st.write(":violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
        st.write("---")
       
        
        st.markdown(":blue[*Download transformed pulse data file below for reference*]")
        
        col3,col4,col5=st.columns(3)
        
        with col3:
            st.download_button("agg_ins","C:/Users/Admin/Desktop/myproject/agg_ins.csv/")
            st.download_button("agg_trans","C:/Users/Admin/Desktop/myproject/agg_trans.csv/")
            st.download_button("agg_user","C:/Users/Admin/Desktop/myproject/agg_user.csv/")

        with col4:
            st.download_button("map_ins","C:/Users/Admin/Desktop/myproject/map_ins.csv/")
            st.download_button("map_trans","C:/Users/Admin/Desktop/myproject/map_trans.csv/")
            st.download_button("map_user","C:/Users/Admin/Desktop/myproject/map_user.csv/")

        with col5:
            st.download_button("top_ins","C:/Users/Admin/Desktop/myproject/top_ins.csv/")
            st.download_button("top_trans","C:/Users/Admin/Desktop/myproject/top_trans.csv/")
            st.download_button("top_user","C:/Users/Admin/Desktop/myproject/top_user.csv/")
   
# Aggregated - Aggregated values of various payment categories.
# Map - Total values at the State and District levels.
# Top - Totals of top States / Districts /Pin Codes


# # setting up menu - explore data
if select_page == "Explore Data":
    Type = st.sidebar.selectbox("*Type*", ("Transactions", "Users","Insurance"))
    Year = st.sidebar.slider("*Year*", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("*Quarter*", min_value=1, max_value=4)
    
    col1,col2 = st.columns(2)
    
# transaction data exploration
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :blue[State Data - Transactions Amount]")
            cursor.execute(f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            
        #geojson- geoJSON data source for indias state boundaries
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',   #key in geoJSON file for thr state names
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')
              
        #update_geos- updates props of geo layout, fitbounds- adjust the state boundaries and ensures all locations given are visible within viewport
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :blue[State Data - Transactions Count]")
            cursor.execute(f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df1.Total_Transactions = df1.Total_Transactions.astype(float)
            

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# visualizations - TOP PAYMENT TYPE
        
        st.markdown("## :blue[Top Payment Type]")
        cursor.execute(f"select transaction_type, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from agg_transaction where year= {Year} and quater = {Quarter} group by transaction_type order by transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])
        fig = px.pie(df,
                    title='Transaction Types Distribution',
                    names='Transaction_type',
                    values='Total_Transactions',
                    color='Total_amount',
                    color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)

# visualizations TRANSACTIONS - DISTRICT WISE DATA            
        
        st.markdown("## :blue[Select a State from below to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
       'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
       'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal', 'Dadra & Nagar Haveli & Daman & Diu',
       'Dadra And Nagar Haveli And Daman And Diu'),index=30)
         
        cursor.execute(f"select state, districts,year,quater, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} and state = '{selected_state}' group by state, districts,year,quater order by state,districts")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state + " - District vs Total_Transactions",
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
#  user data exploration   
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :blue[State Data - User App opening frequency]")
        cursor.execute(f"select state, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
       
        if Year == 2018 and  Quarter in [1,2,3,4]:
            st.warning(" :blue[No Records to Display]" ,icon="🚨")
        else:    
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Appopens',
                      color_continuous_scale='sunset')
    
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :blue[Select any State below to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
       'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
       'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal', 'Dadra & Nagar Haveli & Daman & Diu',
       'Dadra And Nagar Haveli And Daman And Diu'),index=30)
        
        cursor.execute(f"select state,year,quater,districts,sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} and state = '{selected_state}' group by state, districts,year,quater order by state,districts")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state + " - District vs Total_users",
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Inferno)
        st.plotly_chart(fig,use_container_width=True)
     
     
    if Type == "Insurance":
        
        # Overall State Data - INSURANCE TYPE - INDIA MAP
        st.markdown("## :blue[State Data - Insurance User - Transaction count ]")
        
        
        if Year == 2018 and  Quarter in [1,2,3,4]:
            st.warning(" :blue[No Records to Display]" ,icon="🚨")
        
        elif Year == 2019 and Quarter in [1,2,3,4]:
            st.warning(" :blue[No Records to Display] " ,icon="🚨") 
            
        elif  Year == 2020 and Quarter in [1]:
            st.warning(" :blue[No Records to Display} ",icon="🚨") 
            
        else:
        
            cursor.execute(f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_insurance where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions','Total_amount'])
          
            # df1.Total_Transactions = df1.Total_Transactions.astype(int)
            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            #overall state transaction amount data in map insurance
            st.markdown("## :blue[State Data - Insurance user- Transaction Amount]")
            cursor.execute(f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_insurance where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            
            df1.Total_amount = df1.Total_amount.astype(int)
            

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_amount',
                        color_continuous_scale='inferno')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        
# MENU 3 - 
if select_page == "Insights":
     
    st.markdown("## :blue[Insights from data]")
    Type = st.sidebar.selectbox("*Type*", ("Transactions", "Users","Insurance"))
    Year = st.sidebar.slider("*Year*", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("*Quarter*", min_value=1, max_value=4)
   
   # Transaction insight
   
    if Type == "Transactions":
    
        st.info(
                """
                - Highest Number of State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Highest Number of State, District based on Total phonepe users and their app opening frequency.
                - Top 10 states ,districts , pin codes where the most number of the insurance happened for a selected year-quarter combination.
                - Top 10 mobile brands and its percentage based on the phonepe users.
                """
                )
        tab1,tab2,tab3= st.tabs(["$\huge STATE $",  "$\huge DISTRICT $",   "$\huge PINCODE $"])   
   
    
        with tab1:
                
                cursor.execute(f"select state, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from agg_transaction where year = {Year} and quater = {Quarter} group by state order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                
                fig = px.bar(df,
                            x='State',
                            y='Total_Amount',
                            orientation='v',
                            title='Highest 10 States by Total Amount',
                            color='Transactions_Count',
                            color_continuous_scale=px.colors.sequential.Inferno,
                            labels={'Transactions_Count': 'Transactions Count'})

                fig.update_layout(xaxis_title='State', yaxis_title='Total Amount')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            
            cursor.execute(f"select districts , sum(transaction_count) as Total_Count, sum(transaction_amount) as Total from map_transaction where year = {Year} and quater = {Quarter} group by districts order by Total desc limit 5")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Highest 5 District by Total_amount',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with tab3:
            
            cursor.execute(f"select pincodes, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from top_transaction where year = {Year} and quater = {Quarter} group by pincodes order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Highest 10 pincodes by Total_amount',
                             color_discrete_sequence=px.colors.sequential.Inferno,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# users insights   
    if Type == "Users":
       
        tab1,tab2,tab3= st.tabs(["$\huge BRANDS $",  "$\huge DISTRICT $",   "$\huge STATE $"])
        with tab1:
           
            if Year == 2022 and  Quarter in [2,3,4]:
               st.warning(" :blue[No Records to Display] ",icon="🚨")
            
            elif Year == 2023 and Quarter in [1,2,3,4]:
                st.warning(" :blue[No Records to Display] ",icon="🚨")   
            else:
                cursor.execute(f"select brands, sum(transaction_count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quater = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                                title='Top 10 brands by total_users',
                                x="Total_Users",
                                y="Brand",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
        
        with tab2:
            
            cursor.execute(f"select districts, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 districts by total_users',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Inferno)
            st.plotly_chart(fig,use_container_width=True)
              
        
        with tab3:
            
            cursor.execute(f"select state, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10 states by total_users',
                             color_discrete_sequence=px.colors.sequential.Inferno_r,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
            
# Insurance insights
    if Type == "Insurance":
         tab1,tab2,tab3= st.tabs(["$\huge STATE $",  "$\huge DISTRICT $",   "$\huge PINCODE $"])   
   
    
         with tab1:
                
            if Year == 2018 and  Quarter in [1,2,3,4]:
                st.warning(" :blue[No Records to Display] ",icon="🚨")
            
            elif Year == 2019 and Quarter in [1,2,3,4]:
               st.warning(" :blue[No Records to Display] ",icon="🚨")
                
            elif  Year == 2020 and Quarter in [1]:
               st.warning(" :blue[No Records to Display] ",icon="🚨") 
                
        
            else:   
                cursor.execute(f"select state, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from agg_insurance where year = {Year} and quater = {Quarter} group by state order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                
                fig = px.bar(df,
                            x='State',
                            y='Total_Amount',
                            orientation='v',
                            title='Highest 10 States by Total Amount',
                            color='Transactions_Count',
                            color_continuous_scale=px.colors.sequential.Inferno,
                            labels={'Transactions_Count': 'Transactions Count'})

                fig.update_layout(xaxis_title='State', yaxis_title='Total Amount')
                st.plotly_chart(fig, use_container_width=True)

         with tab2:
             
            
            if Year == 2018 and  Quarter in [1,2,3,4]:
                st.warning(" :blue[No Records to Display] ",icon="🚨")
            
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.warning(" :blue[No Records to Display] ",icon="🚨")
                
            elif  Year == 2020 and Quarter in [1]:
                st.warning(" :blue[No Records to Display] ",icon="🚨") 
                
            else:   
                cursor.execute(f"select districts , sum(transaction_count) as Total_Count, sum(transaction_amount) as Total from map_insurance where year = {Year} and quater = {Quarter} group by districts order by Total desc limit 5")
                df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Highest 5 District by Total_amount',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
         with tab3:
             
              
            if Year == 2018 and  Quarter in [1,2,3,4]:
               st.warning(" :blue[No Records to Display]",icon="🚨")
            
            elif Year == 2019 and Quarter in [1,2,3,4]:
               st.warning(" :blue[No Records to Display] ",icon="🚨")
                
            elif  Year == 2020 and Quarter in [1]:
               st.warning(" :blue[No Records to Display] ",icon="🚨")
                
            else:
                
                cursor.execute(f"select pincodes, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from top_insurance where year = {Year} and quater = {Quarter} group by pincodes order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Highest 10 pincodes by Total_amount',
                                color_discrete_sequence=px.colors.sequential.Inferno,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
