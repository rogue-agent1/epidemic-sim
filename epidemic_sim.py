#!/usr/bin/env python3
"""epidemic_sim - SIR/SEIR epidemic model simulator."""
import sys, json, math

def sir_model(S0, I0, R0, beta, gamma, days):
    N = S0 + I0 + R0; S, I, R = float(S0), float(I0), float(R0)
    history = [{"day": 0, "S": S, "I": I, "R": R}]
    for d in range(1, days+1):
        dS = -beta*S*I/N; dI = beta*S*I/N - gamma*I; dR = gamma*I
        S += dS; I += dI; R += dR
        history.append({"day": d, "S": round(S), "I": round(I), "R": round(R)})
    return history

def seir_model(S0, E0, I0, R0, beta, sigma, gamma, days):
    N = S0+E0+I0+R0; S,E,I,R = float(S0),float(E0),float(I0),float(R0)
    history = [{"day": 0, "S": S, "E": E, "I": I, "R": R}]
    for d in range(1, days+1):
        dS = -beta*S*I/N; dE = beta*S*I/N - sigma*E
        dI = sigma*E - gamma*I; dR = gamma*I
        S += dS; E += dE; I += dI; R += dR
        history.append({"day": d, "S": round(S), "E": round(E), "I": round(I), "R": round(R)})
    return history

def r0(beta, gamma):
    return beta / gamma

def peak_infections(history):
    return max(history, key=lambda x: x["I"])

def herd_immunity_threshold(R0):
    return 1 - 1/R0 if R0 > 1 else 0

def main():
    print("Epidemic simulation demo\n")
    pop = 100000; beta = 0.3; gamma = 0.1
    R0 = r0(beta, gamma)
    print(f"  R0 = {R0:.1f}, Herd immunity threshold: {herd_immunity_threshold(R0)*100:.0f}%")
    sir = sir_model(pop-10, 10, 0, beta, gamma, 200)
    peak = peak_infections(sir)
    print(f"\n  SIR (β={beta}, γ={gamma}):")
    print(f"    Peak: day {peak['day']}, {peak['I']} infected")
    print(f"    Final: {sir[-1]['R']} recovered, {sir[-1]['S']} susceptible")
    seir = seir_model(pop-10, 0, 10, 0, beta, 0.2, gamma, 200)
    peak2 = peak_infections(seir)
    print(f"\n  SEIR (σ=0.2 incubation):")
    print(f"    Peak: day {peak2['day']}, {peak2['I']} infected")

if __name__ == "__main__":
    main()
