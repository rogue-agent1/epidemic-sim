#!/usr/bin/env python3
"""SIR epidemic model simulation."""
def sir(S0=999,I0=1,R0=0,beta=0.3,gamma=0.1,days=160):
    N=S0+I0+R0;S,I,R=float(S0),float(I0),float(R0);history=[]
    for d in range(days):
        history.append({"day":d,"S":int(S),"I":int(I),"R":int(R)})
        dS=-beta*S*I/N;dI=beta*S*I/N-gamma*I;dR=gamma*I
        S+=dS;I+=dI;R+=dR
    return history
def seir(S0=999,E0=0,I0=1,R0=0,beta=0.3,sigma=0.2,gamma=0.1,days=200):
    N=S0+E0+I0+R0;S,E,I,R=float(S0),float(E0),float(I0),float(R0);history=[]
    for d in range(days):
        history.append({"day":d,"S":int(S),"E":int(E),"I":int(I),"R":int(R)})
        dS=-beta*S*I/N;dE=beta*S*I/N-sigma*E;dI=sigma*E-gamma*I;dR=gamma*I
        S+=dS;E+=dE;I+=dI;R+=dR
    return history
if __name__=="__main__":
    h=sir();peak=max(h,key=lambda x:x["I"])
    print(f"SIR: peak infections={peak['I']} on day {peak['day']}")
    print(f"R0={0.3/0.1:.1f}")
    h2=seir();peak2=max(h2,key=lambda x:x["I"])
    print(f"SEIR: peak={peak2['I']} on day {peak2['day']}")
    print("Epidemic sim OK")
