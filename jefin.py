import math
import matplotlib.pyplot as plt

def run_energy_audit():
    print("*"*50)
    print("DIGITAL ENERGY AUDIT & PF CALCULATOR")
    print("*"*50)

    #User inputs
    system_type=input("System phase configuration(s=Single phase,3=Three phase):")
    voltage=float(input("Enter The System Voltage(V):"))
    current=float(input("Enter The System Current(A):"))
    pf_initial=float(input("Enter Target Power Factor(PF):"))#cosphi1
    pf_target=float(input("Enter The Target Power Factor:"))#cosphi2
    electricity_rate=float(input("Enter the electricity rate per kWh(₹)[eg.8.0]:"))
    operating_hours=float(input("Enter monthly operating hours:"))
    if system_type.upper()=="S":
        apparent_power_s1=(voltage*current)/1000.0
    else:
        apparent_power_s1=(math.sqrt(3)*voltage*current)/1000.0
    
    
    #1.Electrical Power Calculations
 
    active_power_p=apparent_power_s1*pf_initial#kW

    phi1=math.acos(pf_initial)
    q1_kvar=apparent_power_s1*math.tan(phi1)#initial kVAR

    phi2=math.acos(pf_target)
    q2_kvar=active_power_p*math.tan(phi2)#final kVAR
    

    #2.Required Capacitor Bank Compensation(kVAR)

    qc_required=q1_kvar-q2_kvar
    #Financial & Demand reduction calculations
    apparent_power_s2=active_power_p/pf_target
    kva_reduced=apparent_power_s1-apparent_power_s2
    monthly_savings=kva_reduced*operating_hours*electricity_rate
    annual_savings=monthly_savings*12

    print("\n"+"*"*50)
    print("AUDIT SUMMARY")
    print("*"*50)
    print(f"Active Power (P):{active_power_p:.2f} kVA")
    print(f"Initial Apparent Power(S1):{apparent_power_s1:.2f}kVA")
    print(f"Traget Reactive Power(Q1):{q1_kvar:.2f}kVAR")
    print(f"Target Reactive Power(Q2):{q2_kvar:.2f}kVAR")
    print("*"*50)
    print(f"CAPACITOR BANK REQUIRED:{max(0.0,qc_required):.2f}kVAR")


    #3.Plotting Power Triangle Graph
    plt.figure(figsize=(8,6))

    #Active Power(Base)
    plt.plot([0,active_power_p],[0,0],'b-',linewidth=3,label=f"Active Power(P)={active_power_p:.2f}kW")

    #Initial State(Q1&S1)
    plt.plot([active_power_p,active_power_p],[0,q1_kvar],"r--",linewidth=2,label=f"initial Q1={q1_kvar:.2f}kVar")
    plt.plot([0,active_power_p],[0,q1_kvar],'r--',linewidth=1.5,label=f"Initial S1(PF={pf_initial})")

    #Corrected State (Q2 & S2)
    plt.plot([active_power_p, active_power_p], [0, q2_kvar], 'g-', linewidth=3, label=f'Target Q2 = {q2_kvar:.2f} kVAR')
    plt.plot([0, active_power_p], [0, q2_kvar], 'g-', linewidth=2, label=f'Target S2 (PF = {pf_target})')

    # Graph Formatting
    plt.title('Power Factor Correction - Electrical Power Triangle', fontsize=12, fontweight='bold')
    plt.xlabel('Active Power (kW)', fontsize=10)
    plt.ylabel('Reactive Power (kVAR)', fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Show Figure
    plt.show()
if __name__ == "__main__":
      run_energy_audit()

    
