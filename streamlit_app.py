import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#Database connection
engine = create_engine("mysql+pymysql://root:@localhost/datascience")

#Page Setup
st.set_page_config(page_title="Police Stop Dashboard", layout="centered")

#Landing Page
st.title("🚔 Police Stop Analysis Dashboard")
st.markdown("**Developed by 🪻 Ashwin T**")
st.write("---")

#Main Buttons
st.markdown("### Get Started✅")
st.write("\n")
col1, col2 = st.columns(2)
st.write("---")
st.write("\n")


with col1:
    analysis_btn = st.button("📊 Pick an Analysis", use_container_width=True)
    content_placeholder = st.empty()
with col2:
    predict_btn = st.button("📝 Add New Violation & Predict Outcome", use_container_width=True)

#Navigation Logic
if analysis_btn:
    st.session_state["page"] = "analysis"
elif predict_btn:
    st.session_state["page"] = "predict"

page = st.session_state.get("page", None)

# ANALYSIS PAGE
if page == "analysis":
    st.header("📊 Choose Your Analysis")

    user_choice = st.selectbox(
        "🛑 Pick an Analysis : ",
        [
            "Top 10 Vehicles in Drug Related Stops",
            "Most Frequently searched Vehicle",
            "Most Arrested Driver Age Group",
            "Gender Distribution of Drivers stopped in Each Country",
            "Race - Gender Combination with Highest Search Rate",
            "Time of the Day sees the Most Stops",
            "Average stop duration per Violation",
            "Compare Arrest Rates: Day vs. Night",
            "Violation Escalation Rate (Search OR Arrest)",
            "Violations by Younger Drivers",
            "Violations with the Lowest Search/Arrest Association",
            "Identifying Countries with the Most Drug-Related Stops",
            "Arrest Rate Breakdown by Country AND Violation",
            "Country with the highest number of traffic stops with a search conducted",
            #Complex Query
            "Yearly Breakdown of Stops and Arrests by Country",
            "Driver Violation Based on Age and Race",
            "Time Period Analysis of Stops",
            "Violations with High Search and Arrest Rates",
            "Driver Demographics by Country (Age, Gender, and Race)",
            "Top 5 Violations with Highest Arrest Rates"
        ]
    )

    query = ""

    if user_choice == "Top 10 Vehicles in Drug Related Stops":
        query = """
            SELECT 
                vehicle_number, 
                COUNT(*) AS total_stops
            FROM police_stops
            WHERE drugs_related_stop = 'TRUE'
            GROUP BY vehicle_number
            ORDER BY total_stops DESC
            LIMIT 10;
        """

    elif user_choice == "Most Frequently searched Vehicle":
        query = """
            SELECT 
                vehicle_number, 
                COUNT(*) AS most_searched
            FROM police_stops
            WHERE search_conducted = 'TRUE'
            GROUP BY vehicle_number
            ORDER BY most_searched DESC 
            LIMIT 5;
        """

    elif user_choice == "Most Arrested Driver Age Group":
        query = """
            SELECT
                CASE
                    WHEN driver_age < 20 THEN 'Teens'
                    WHEN driver_age >= 20 AND driver_age < 30 THEN 'Young'
                    WHEN driver_age >= 30 AND driver_age < 50 THEN 'Middle Aged'
                    WHEN driver_age >= 50 AND driver_age < 60 THEN 'Fifties'
                    WHEN driver_age >= 60 THEN 'Old Age'
                END AS age_group,
                COUNT(*) AS total_drivers,
                SUM(is_arrested = 'TRUE') AS total_drivers_arrested,
                AVG(is_arrested = 'TRUE') * 100 AS arrest_rate_percentage
            FROM police_stops
            GROUP BY age_group
            ORDER BY arrest_rate_percentage DESC
            LIMIT 1;
        """

    elif user_choice == "Gender Distribution of Drivers stopped in Each Country":
        query = """
            SELECT 
                country_name,
                SUM(driver_gender = 'M') AS Male_Driver,
                SUM(driver_gender = 'F') AS Female_Driver
            FROM police_stops
            WHERE search_conducted = 'TRUE'
            GROUP BY country_name;
        """

    elif user_choice == "Race - Gender Combination with Highest Search Rate":
        query = """
            SELECT
                driver_race,
                SUM(driver_gender = 'M') AS Male_Searches,
                SUM(driver_gender = 'F') AS Female_Searches,
                AVG(search_conducted = 'TRUE') * 100 AS Search_Rate_Percent
            FROM police_stops
            GROUP BY driver_race
            ORDER BY Search_Rate_Percent DESC
            LIMIT 5;
        """

    elif user_choice == "Time of the Day sees the Most Stops":
        query = """
            SELECT HOUR(stop_time) AS stop_hour, 
                COUNT(*) AS total_stops
            FROM police_stops
            GROUP BY HOUR(stop_time)
            ORDER BY total_stops DESC LIMIT 15;
        """

    elif user_choice == "Average stop duration per Violation":
        query = """
            SELECT
                violation,
                SUM( stop_duration = '0-15 Min' ) AS 0_15_Min,
                SUM(stop_duration = '16-30 Min' ) AS 16_30_Min,
                SUM(stop_duration = '30+ Min' ) AS 30_Plus_Min,
                AVG(
                    CASE
                        WHEN stop_duration = '0-15 Min'  THEN 7.5   
                        WHEN stop_duration = '16-30 Min' THEN 23.0 
                        WHEN stop_duration = '30+ Min'   THEN 45.0  
                    END
                ) AS Average_Duration_Minutes
            FROM police_stops            
            GROUP BY violation
            ORDER BY Average_Duration_Minutes DESC;
        """

    elif user_choice == "Compare Arrest Rates: Day vs. Night":
        query = """
            SELECT
                CASE
                    WHEN ( HOUR(stop_time) >= 7 AND HOUR(stop_time) <= 18 )
                    THEN 'Day'
                    ELSE 'Night'
                END AS Time_of_Day,
                COUNT(*) AS Total_Stops,
                SUM( is_arrested = 'TRUE') AS Total_Arrests,
                AVG(is_arrested = 'TRUE') * 100.0 AS Arrest_Rate_Percent
            FROM police_stops
            GROUP BY Time_of_Day
            ORDER BY Arrest_Rate_Percent DESC;
        """

    elif user_choice == "Violation Escalation Rate (Search OR Arrest)":
        query = """
            SELECT
                violation,
                AVG(search_conducted = 'TRUE') * 100 AS Search_Rate_Percent,
                AVG(is_arrested = 'TRUE') * 100 AS Arrest_Rate_Percent
            FROM police_stops 
            GROUP BY violation
            ORDER BY Search_Rate_Percent DESC;
        """  
   

    elif user_choice == "Violations by Younger Drivers":
        query = """
            SELECT
                violation,
                COUNT(*) AS Violations_by_Younger_Drivers
            FROM police_stops 
            WHERE driver_age < 25       
            GROUP BY violation             
            ORDER BY  Violations_by_Younger_Drivers DESC
            LIMIT 5;
        """  
    elif user_choice == "Violations with the Lowest Search/Arrest Association":
        query = """
            SELECT 
                violation,
                SUM(is_arrested = 'TRUE') AS Total_Arrests,
                SUM(is_arrested = 'TRUE') / COUNT(*) * 100 AS Arrest_Rate_Percent,
                SUM(search_conducted = 'TRUE') AS Total_Searches,
                SUM(search_conducted = 'TRUE') / COUNT(*) * 100 AS Search_Rate_Percent

            FROM police_stops
            GROUP BY violation
            ORDER BY Search_Rate_Percent ASC, Arrest_Rate_Percent ASC
            LIMIT 5;
        """  

    elif user_choice == "Identifying Countries with the Most Drug-Related Stops":
        query = """
            SELECT 
                country_name,
                COUNT(*) AS Total_Stops,
                SUM(drugs_related_stop = 'TRUE') AS Total_Drug_Stops,
                AVG(drugs_related_stop = 'TRUE') * 100 AS Drug_Stop_Rate_Percent
            FROM police_stops
            GROUP BY country_name
            ORDER BY Drug_Stop_Rate_Percent DESC
            LIMIT 5;

    """

    elif user_choice == "Arrest Rate Breakdown by Country AND Violation":
        query = """
            SELECT 
                country_name,
                violation,
                COUNT(*) AS total_stops,
                SUM(is_arrested ='TRUE') AS total_arrested,
                ROUND(AVG(is_arrested ='TRUE')*100, 2) AS arrest_rate
            FROM police_stops 
            GROUP BY country_name, violation
            ORDER BY country_name ASC;

    """   

    elif user_choice == "Country with the highest number of traffic stops with a search conducted":
        query = """
            SELECT 
                COUNT(*) AS total_stops,
                SUM(search_conducted = 'TRUE') AS total_searches
            FROM police_stops 
            GROUP BY country_name
            ORDER BY total_searches DESC;

    """
 #COMPLEX

    elif user_choice == "Yearly Breakdown of Stops and Arrests by Country":
        query = """
            SELECT
                country_name,
                year,
                total_stops,
                total_arrests,
                RANK() OVER (PARTITION BY year ORDER BY total_stops DESC) AS stop_rank
            FROM
            (
                SELECT
                    country_name,
                    YEAR(stop_date) AS year,
                    COUNT(*) AS total_stops,
                    SUM(is_arrested='TRUE') AS total_arrests
                FROM police_stops
                GROUP BY country_name, YEAR(stop_date)
            ) AS summary
            ORDER BY year, stop_rank;

    """


    elif user_choice == "Driver Violation Based on Age and Race":
        query = """
            SELECT *
                FROM (
                    SELECT
                        driver_race, violation,
                        CASE
                            WHEN driver_age < 20 THEN 'Teens'
                            WHEN driver_age BETWEEN 20 AND 35 THEN 'Young'
                            WHEN driver_age BETWEEN 35 AND 50 THEN 'Middle aged'
                            ELSE '50+'
                        END AS age_group,
                        COUNT(*) AS total_violations
                    FROM police_stops
                    GROUP BY 
                    driver_race, 
                    violation,
                    age_group 
                ) AS subquery
                ORDER BY total_violations DESC;

    """


    elif user_choice == "Time Period Analysis of Stops":
        query = """
           SELECT
                YEAR(stop_date) AS year,         
                MONTH(stop_date) AS month,      
                HOUR(stop_time) AS hour_of_day,   
                COUNT(*) AS total_stops          
            FROM police_stops
            GROUP BY
                YEAR(stop_date),
                MONTH(stop_date),
                HOUR(stop_time)
            ORDER BY
                year,
                month,
                hour_of_day;
    """
        
    elif user_choice == "Violations with High Search and Arrest Rates":
        query = """
            SELECT 
                violation,
                COUNT(*) AS total_stops,
                SUM(search_conducted = 'TRUE') AS total_searches,
                SUM(is_arrested = 'TRUE') AS total_arrests,
                
                AVG(search_conducted = 'TRUE') * 100 AS search_rate_percent,
                AVG(is_arrested = 'TRUE') * 100 AS arrest_rate_percent,
                
                RANK() OVER (ORDER BY (AVG(search_conducted = 'TRUE')*100) DESC) AS search_rank,
                RANK() OVER (ORDER BY (AVG(is_arrested = 'TRUE')*100) DESC) AS arrest_rank

            FROM police_stops
            GROUP BY violation
            ORDER BY arrest_rate_percent DESC;
    """      
            
    elif user_choice == "Driver Demographics by Country (Age, Gender, and Race)":
        query = """
            SELECT 
                country_name,
                AVG(driver_age) AS avg_age,
                MIN(driver_age) AS min_age,
                MAX(driver_age) AS max_age,
                SUM(driver_gender = 'M') AS male_drivers,
                SUM(driver_gender = 'F') AS female_drivers,
                SUM(driver_race = 'Asian') AS asian_drivers,
                SUM(driver_race = 'Hispanic') AS hispanic_drivers,
                SUM(driver_race = 'Black') AS black_drivers,
                SUM(driver_race = 'White') AS white_drivers,
                SUM(driver_race = 'Other') AS other_drivers
            FROM 
                police_stops
            GROUP BY 
                country_name
            ORDER BY 
                country_name;
    """
        
    elif user_choice == "Top 5 Violations with Highest Arrest Rates":
        query = """
            SELECT 
                violation,
                COUNT(*) AS total_stops,
                SUM(is_arrested='TRUE') AS total_arrests,
                AVG(is_arrested='TRUE')*100 AS arrest_rate
            FROM 
                police_stops
            GROUP BY 
                violation
            ORDER BY 
                arrest_rate DESC;
    """

    #Query Execution
    if query:
        try:
            df = pd.read_sql(query, con=engine)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ Error running query: {e}")

#PREDICTION PAGE
elif page == "predict":
    st.header("📝 Add New Violation & Predict Outcome")
    st.write("✏️Enter details below to predict the likely outcome:")

with st.form("violation_form"):
    st.markdown("### 🚗 Violation Details Entry Form")

    #Basic Details
    date = st.date_input("Date of Stop")
    time = st.time_input("Time of Stop")
    country = st.selectbox("Country", ["Canada", "India", "USA"])
    vehicle_number = st.text_input("Vehicle Number", "TN01AB1234")

    #Driver Details
    driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
    driver_age = st.number_input("Driver Age", step=1)
    driver_race = st.selectbox("Driver Race",["Other", "Asian", "Black", "Hispanic", "White"])

    #Violation Details
    violation = st.selectbox("Violation Type",["Other", "Drunk Driving", "Signal Violation", "Seatbelt", "Speeding"])
    search_conducted = st.selectbox("Search Conducted?", ["FALSE", "TRUE"])
    search_type = st.selectbox("Search Type",["None", "Frisk", "Vehicle Search"])
    drugs_related_stop = st.selectbox("Drugs Related Stop?", ["FALSE", "TRUE"])
    stop_duration = st.selectbox("stop_duration", ["0-15 Min", "16-30 Min", "30+ Min"])

    #Submit Button
    submitted = st.form_submit_button("Predict Outcome")


if submitted:
    # Prediction
    violation_lower = violation.lower()
    if (search_conducted == "TRUE" and drugs_related_stop == "TRUE") or violation_lower == "drunk driving":
        predicted_outcome = "Arrested"
    elif driver_age < 18:
        predicted_outcome = "Warning"
    elif violation_lower in ["seatbelt", "speeding", "signal violation"]:
        predicted_outcome = "Warning"
    else:
        predicted_outcome = "No Action"

    st.success(f"✅ Predicted Outcome: **{predicted_outcome}**")

    #Option to save
    save = st.checkbox("Save this record to database")
    if save:
        try:
            insert_query = f"""
                INSERT INTO police_stops (
                    date, time, country_name, vehicle_number,
                    driver_gender, driver_age, driver_race, violation,
                    search_conducted, search_type, drugs_related_stop,
                    stop_duration, stop_outcome
                ) VALUES (
                    '{date}', '{time}', '{country}', '{vehicle_number}',
                    '{driver_gender}', {driver_age}, '{driver_race}', '{violation}',
                    '{search_conducted}', '{search_type}', '{drugs_related_stop}',
                    '{stop_duration}', '{predicted_outcome}'
                );
            """
            with engine.begin() as conn:
                conn.execute(insert_query)
            st.info("🗂️ Record added successfully.")
        except Exception as e:
            st.error(f"Error saving record: {e}")
