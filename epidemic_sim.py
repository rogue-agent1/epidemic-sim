#!/usr/bin/env python3
"""SIR epidemic model simulation."""
import sys
def sir(S0,I0,R0,beta,gamma,days):
    N=S0+I0+R0;S,I,R=float(S0),float(I0),float(R0)
    history=[(0,S,I,R)]
    for d in range(1,days+1):
        dS=-beta*S*I/N;dI=beta*S*I/N-gamma*I;dR=gamma*I
        S+=dS;I+=dI;R+=dR
        history.append((d,S,I,R))
    return history
def main():
    pop=10000;infected=10;beta=0.3;gamma=0.1
    R0=beta/gamma
    print(f"SIR Model: pop={pop}, I0={infected}, β={beta}, γ={gamma}, R0={R0:.1f}")
    history=sir(pop-infected,infected,0,beta,gamma,160)
    print(f"\n{'Day':>4} {'S':>7} {'I':>7} {'R':>7}")
    for d,S,I,R in history[::10]:
        bar='▓'*int(I/200)
        print(f"{d:4.0f} {S:7.0f} {I:7.0f} {R:7.0f} {bar}")
    peak=max(history,key=lambda x:x[2])
    print(f"\nPeak infection: day {peak[0]}, {peak[2]:.0f} infected ({peak[2]/pop*100:.1f}%)")
if __name__=="__main__": main()
