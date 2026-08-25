import streamlit as st
import matplotlib.pyplot as plt
import math

# Page Configuration
st.set_page_config(page_title="Power Factor Correction Calculator", page_icon="⚡", layout="wide")

st.title("⚡ Power Factor Correction & Savings Calculator")
st.write("Enter your electrical parameters below to calculate capacitor sizing and view visual power triangles.")

st.markdown("---")

# Main Input Section
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. System Details")
    phase_type = st.radio("System Type", ["Single-Phase", "Three-Phase"], horizontal=True)
    
    # Voltage Input with + / - buttons
    voltage = st.number_input("Operating Voltage (V)", value=230.0, step=10.0, help="Standard single-phase is ~230V, 3-phase is ~415V")
    
    # Current Input with + / - buttons
    current = st.number_input("Line Current (Amps)", value=15.0, step=1.0)

with col_right:
    st.subheader("2. Bill & Usage Details")
    
    # Electricity Rate Input
    unit_rate = st.number_input("Electricity Rate per Unit / kWh (₹)", value=6.5, step=0.5)
    
    # Monthly Hours Input
    hours_per_month = st.number_input("Monthly Operating Hours", value=300, step=10, help="e.g., 10 hours/day for 30 days = 300 hours")

st.markdown("---")

st.subheader("3. Power Factor Settings")
pf_col1, pf_col2 = st.columns(2)

with pf_col1:
    # Initial PF Input
    initial_pf = st.number_input("Current Power Factor (PF1)", min_value=0.10, max_value=0.99, value=0.75, step=0.01)

with pf_col2:
    st.write("Target Power Factor (PF2)")
    
    # Preset Selection Buttons for fast selection
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    
    # Session state initialization for target_pf
    if 'target_pf_val' not in st.session_state:
        st.session_state.target_pf_val = 0.98

    if preset_col1.button("0.95"):
        st.session_state.target_pf_val = 0.95
    if preset_col2.button("0.98 (Ideal)"):
        st.session_state.target_pf_val = 0.98
    if preset_col3.button("1.00 (Max)"):
        st.session_state.target_pf_val = 1.00

    # Number input field tied to the selected value or manual entry
    target_pf = st.number_input("Selected Target PF", min_value=0.10, max_value=1.00, value=st.session_state.target_pf_val, step=0.01, key="target_pf_input")

st.markdown("---")

# Large Action Button
if st.button("🚀 Calculate Energy Audit & Sizing", type="primary", use_container_width=True):
    if initial_pf >= target_pf:
        st.error("Target Power Factor must be greater than Current Power Factor!")
    else:
        # Calculations
        multiplier = 1.0 if phase_type == "Single-Phase" else math.sqrt(3)
        frequency = 50.0  # Hz
        
        # Active Power P (kW)
        active_power_kw = (multiplier * voltage * current * initial_pf) / 1000.0
        
        # Initial & Target Reactive Power Q (kVAR)
        phi1 = math.acos(initial_pf)
        phi2 = math.acos(target_pf)
        q1 = active_power_kw * math.tan(phi1)
        q2 = active_power_kw * math.tan(phi2)
        
        # Required Capacitor Bank Compensation Rating
        qc_kvar = q1 - q2
        
        # Physical Capacitance (in uF)
        capacitance_uf = (qc_kvar * 1000 * 10**6) / (2 * math.pi * frequency * (voltage**2))
        
        # Apparent Power Drop (kVA)
        s1_kva = active_power_kw / initial_pf
        s2_kva = active_power_kw / target_pf
        kva_saved = s1_kva - s2_kva
        
        # Monthly Energy Consumption
        monthly_kwh = active_power_kw * hours_per_month
        monthly_cost = monthly_kwh * unit_rate

        # Results Display Section
        st.header("📊 Audit Results & Sizing Summary")
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Active Load (P)", f"{active_power_kw:.2f} kW")
        m_col2.metric("Capacitor Rating (Qc)", f"{qc_kvar:.2f} kVAR")
        m_col3.metric("Required Capacitance", f"{capacitance_uf:.2f} µF")
        m_col4.metric("Demand Drop", f"{kva_saved:.2f} kVA")

        # Plotting Power Triangle
        st.subheader("📐 Power Triangle Comparison")
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Active Power Line
        ax.plot([0, active_power_kw], [0, 0], color='black', linewidth=3, label='Active Power P (kW)')
        
        # Uncorrected Vector
        ax.plot([active_power_kw, active_power_kw], [0, q1], color='red', linestyle='--', linewidth=2, label=f'Initial Q1 ({q1:.2f} kVAR)')
        ax.plot([0, active_power_kw], [0, q1], color='red', alpha=0.5, label=f'Initial S1 ({s1_kva:.2f} kVA)')
        
        # Corrected Vector
        ax.plot([active_power_kw, active_power_kw], [0, q2], color='green', linestyle='--', linewidth=2, label=f'Target Q2 ({q2:.2f} kVAR)')
        ax.plot([0, active_power_kw], [0, q2], color='green', alpha=0.7, label=f'Target S2 ({s2_kva:.2f} kVA)')

        ax.set_xlabel("Active Power (kW)", fontsize=11)
        ax.set_ylabel("Reactive Power (kVAR)", fontsize=11)
        ax.set_title("Uncorrected vs. Corrected Power Triangle", fontsize=12)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper left")
        
        st.pyplot(fig)
