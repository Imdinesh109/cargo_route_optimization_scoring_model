import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import datetime
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Cargo Route Optimization",
    layout="wide"
)

# ==========================================
# 2. LOAD AI MODEL & ENCODERS
# ==========================================
@st.cache_resource
def load_models():
    try:
        model = joblib.load('cargo_xgboost_model.pkl')
        encoders = joblib.load('cargo_label_encoders.pkl')
        return model, encoders
    except FileNotFoundError:
        st.error("ERROR: Could not find model files. Please ensure 'cargo_xgboost_model.pkl' and 'cargo_label_encoders.pkl' are in the same folder.")
        st.stop()

xgb_model, label_encoders = load_models()

# ==========================================
# 3. LOGICAL MAPPING & CALLBACKS
# ==========================================
CARGO_SHC_MAPPING = {
    "General": ["GEN"],
    "Perishable": ["PER", "ICE", "FRO"],
    "Pharmaceutical": ["ELI", "ICE", "FRO", "PER", "GEN"],
    "Valuable": ["VAL"],
    "Dangerous": ["DGR", "CAO", "ELI"],
    "Heavy": ["HEA", "CAO", "GEN"]
}

def get_weather_and_season(month_num):
    if month_num in [12, 1, 2]: return "Winter", 0.35
    elif month_num in [3, 4]: return "Spring", 0.15
    elif month_num == 5: return "Spring", 0.40  
    elif month_num in [6, 7]: return "Summer", 0.10
    elif month_num == 8: return "Summer", 0.45  
    else: return "Monsoon", 0.50

def handle_date_change():
    new_date = st.session_state.shipment_date
    new_season, new_weather = get_weather_and_season(new_date.month)
    st.session_state.season_val = new_season
    st.session_state.weather_val = float(new_weather)

def handle_cargo_change():
    new_cargo = st.session_state.cargo_type_val
    valid_shcs = CARGO_SHC_MAPPING.get(new_cargo, ["GEN"])
    if valid_shcs:
        st.session_state.shc_val = valid_shcs[0]

if 'init_done' not in st.session_state:
    today = datetime.date.today()
    st.session_state.shipment_date = today
    st.session_state.shipment_time = datetime.time(14, 30) 
    
    init_season, init_weather = get_weather_and_season(today.month)
    st.session_state.season_val = init_season
    st.session_state.weather_val = float(init_weather)
    
    st.session_state.cargo_type_val = "Heavy"
    st.session_state.shc_val = "HEA"
    st.session_state.init_done = True

# ==========================================
# 4. HEADER UI
# ==========================================
st.title("Cargo Route Optimization System")
st.divider()

# ==========================================
# 5. 3-COLUMN DASHBOARD (With Tooltips)
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.date_input("Shipment Date", key="shipment_date", on_change=handle_date_change, 
                  help="Select the departure date. This automatically updates the Season and baseline Weather Risk.")
    
    st.time_input("Shipment Time", key="shipment_time", 
                  help="The local departure time. Impacts operational scoring based on airport shift hours and peak congestion.")
    
    auto_day_name = st.session_state.shipment_date.strftime('%A')
    st.text_input("Calculated Day", value=auto_day_name, disabled=True, 
                  help="Derived automatically from the Shipment Date. Weekends vs Weekdays impact operational capacity.")
    
    origin_options = sorted(list(label_encoders['origin'].classes_))
    route_options = [f"{org}-JED" for org in origin_options]
    default_route_idx = route_options.index("FRA-JED") if "FRA-JED" in route_options else 0
    selected_route = st.selectbox("Route", route_options, index=default_route_idx, 
                                  help="The Origin-Destination pair for this cargo flight. Destination is fixed to JED.")
    
    cargo_type_options = sorted(list(label_encoders['cargo_type'].classes_))
    st.selectbox("Cargo Type", cargo_type_options, key="cargo_type_val", on_change=handle_cargo_change, 
                 help="The primary classification of the goods. Automatically restricts compatible SHC codes.")
    
    priority_options = sorted(list(label_encoders['priority'].classes_))
    default_priority = priority_options.index("Standard") if "Standard" in priority_options else 0
    priority = st.selectbox("Priority Level", priority_options, index=default_priority, 
                            help="Service level agreement. Express prioritizes time; Economy prioritizes cost.")

with col2:
    model_known_shcs = list(label_encoders['shc_code'].classes_)
    allowed_shcs = CARGO_SHC_MAPPING.get(st.session_state.cargo_type_val, model_known_shcs)
    valid_shcs = sorted([shc for shc in allowed_shcs if shc in model_known_shcs])
    st.selectbox("SHC Code", valid_shcs, key="shc_val", 
                 help="Special Handling Code (e.g., PER for Perishable, ICE for Dry Ice). Filters based on Cargo Type.")

    airline_options = sorted(list(label_encoders['airline'].classes_))
    default_airline = airline_options.index("Lufthansa Cargo") if "Lufthansa Cargo" in airline_options else 0
    airline = st.selectbox("Airline", airline_options, index=default_airline, 
                           help="The primary carrier executing the route.")
    
    cargo_weight = st.number_input("Cargo Weight (kg)", min_value=10.0, max_value=15000.0, value=8500.0, step=100.0, 
                                   help="Total chargeable weight of the shipment in kilograms.")
    
    connections = st.selectbox("Number of Connections", [0, 1, 2, 3], index=1, 
                               help="0 = Direct flight. Higher connections reduce cost but lower reliability and increase time.")
    
    distance = st.number_input("Distance (km)", min_value=100.0, max_value=15000.0, value=4200.0, step=100.0, 
                               help="Total flight distance including transit legs.")
    
    transit_time = st.number_input("Total Transit Time (Hours)", min_value=1.0, max_value=100.0, value=14.5, step=0.5, 
                                   help="Gate-to-gate duration including layover times.")

with col3:
    cost = st.number_input("Estimated Cost (SAR)", min_value=0.0, value=24500.0, step=500.0, 
                           help="Total transportation expense in Saudi Riyals (SAR). Lower cost improves the optimization score.")
    
    season_options = sorted(list(label_encoders['season'].classes_))
    st.selectbox("Season", season_options, key="season_val", 
                 help="Operational season. Winter/Monsoon generally carry higher operational penalties.")
    
    st.slider("Weather Risk Score", 0.0, 1.0, key="weather_val", step=0.01, 
              help="Calculated risk of meteorological disruption (0.0 = Clear, 1.0 = Severe). Updates with the date.")
    
    reliability = st.slider("Carrier Reliability Score", 0.0, 1.0, 0.88, step=0.01, 
                            help="Historical on-time and safe delivery performance metric for this carrier/route combination.")
    
    capacity = st.number_input("Available Capacity (kg)", min_value=0.0, value=12000.0, step=500.0, 
                               help="Total unallocated volume remaining on the aircraft. Must exceed Cargo Weight.")
    
    load_factor = st.slider("Load Factor", 0.0, 1.0, 0.78, step=0.01, 
                            help="Percentage of aircraft payload already utilized. High load factors limit operational flexibility.")

st.divider()

# ==========================================
# 6. PREDICTION LOGIC & RESULTS
# ==========================================
_, center_col, _ = st.columns([1, 2, 1])

if center_col.button("Analyze Route", use_container_width=True):
    
    origin, destination = selected_route.split('-')
    
    final_month = st.session_state.shipment_date.strftime('%B')
    final_day = st.session_state.shipment_date.strftime('%A')
    final_hour = st.session_state.shipment_time.hour
    
    # 1. Package inputs into a Dictionary
    input_dict = {
        'origin': [origin],
        'destination': [destination],
        'cargo_type': [st.session_state.cargo_type_val],
        'cargo_weight_kg': [cargo_weight],
        'priority': [priority],
        'airline': [airline],
        'season': [st.session_state.season_val],
        'shc_code': [st.session_state.shc_val],
        'num_connections': [connections],
        'distance_km': [distance],
        'total_transit_time_hours': [transit_time],
        'capacity_available_kg': [capacity],
        'reliability_score': [reliability],
        'weather_risk_score': [st.session_state.weather_val],
        'load_factor': [load_factor],
        'cost_sar': [cost],
        'month': [final_month],
        'day_of_week': [final_day],
        'hour': [final_hour]
    }
    
    df_input = pd.DataFrame(input_dict)
    
    # 2. Encode categorical variables
    categorical_features = ['origin', 'destination', 'cargo_type', 'priority', 'airline', 'season', 'shc_code', 'month', 'day_of_week']
    
    for col in categorical_features:
        df_input[col] = label_encoders[col].transform(df_input[col].astype(str)).astype(int)
            
    # 3. Align columns EXACTLY to match the model's expected training order
    # THIS is the fixed array reflecting the exact order your XGBoost model expects
    features_ordered = [
        'origin', 
        'destination', 
        'cargo_type', 
        'cargo_weight_kg', 
        'cost_sar', 
        'total_transit_time_hours', 
        'capacity_available_kg', 
        'reliability_score', 
        'num_connections', 
        'priority', 
        'airline', 
        'distance_km', 
        'weather_risk_score', 
        'season', 
        'load_factor', 
        'shc_code', 
        'month', 
        'day_of_week', 
        'hour'
    ]
    
    df_ready = df_input[features_ordered]
    
    # 4. Generate prediction with clipping correction
    with st.spinner('Calculating optimization score...'):
        raw_score = xgb_model.predict(df_ready)[0]
        score = max(0.0, min(1.0, float(raw_score)))
    
    # 5. Display Clean Split Layout
    out_col1, out_col2 = st.columns([1.2, 1.0])
    
    with out_col1:
        st.markdown(
            f"""
            <div style="
                font-family: monospace; 
                border: 1px solid #2d3139; 
                padding: 20px; 
                background-color: #0e1117; 
                border-radius: 6px; 
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
                white-space: pre-wrap;
                color: #e0e0e0;
                line-height: 1.5;
            ">REQUESTED RAW METRICS:
-------------------------------------------
Cost (SAR)          : <span style="color: #59b2ff; font-weight: bold;">{cost:,.2f}</span>
Transit Time (hrs)  : <span style="color: #59b2ff; font-weight: bold;">{transit_time:.2f}</span>
Reliability         : <span style="color: #59b2ff; font-weight: bold;">{reliability:.3f}</span>
Capacity Available  : <span style="color: #59b2ff; font-weight: bold;">{capacity:,.2f} kg</span></div>
            """, 
            unsafe_allow_html=True
        )
        
    with out_col2:
        if score >= 0.70:
            gauge_color = "#2efc03" 
        elif score >= 0.40:
            gauge_color = "#fca103" 
        else:
            gauge_color = "#fc0303" 
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            number = {'valueformat': '.4f', 'font': {'size': 24, 'color': gauge_color, 'family': 'monospace'}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "ROUTE OPTIMIZATION LEVEL", 'font': {'size': 14, 'color': '#ffffff', 'family': 'monospace, sans-serif'}},
            gauge = {
                'axis': {'range': [0.0, 1.0], 'tickwidth': 1, 'tickcolor': "#888888", 'tickformat': '.2f'},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': "#2d3139",
                'borderwidth': 1,
                'bordercolor': "#4a4a4a",
                'steps': [
                    {'range': [0.0, 0.40], 'color': 'rgba(252, 3, 3, 0.1)'},
                    {'range': [0.40, 0.70], 'color': 'rgba(252, 161, 3, 0.1)'},
                    {'range': [0.70, 1.00], 'color': 'rgba(46, 252, 3, 0.1)'}
                ]
            }
        ))
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=10),
            height=160,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})