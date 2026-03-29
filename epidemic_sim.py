#!/usr/bin/env python3
"""Epidemic simulation (SIR/SEIR models). Zero dependencies."""
import random, sys

class SIR:
    def __init__(self, pop, infected=1, beta=0.3, gamma=0.1):
        self.S = pop - infected
        self.I = infected
        self.R = 0
        self.N = pop
        self.beta = beta
        self.gamma = gamma
        self.history = {"S": [self.S], "I": [self.I], "R": [self.R]}

    def step(self, dt=1):
        dS = -self.beta * self.S * self.I / self.N * dt
        dI = (self.beta * self.S * self.I / self.N - self.gamma * self.I) * dt
        dR = self.gamma * self.I * dt
        self.S += dS; self.I += dI; self.R += dR
        self.S = max(0, self.S); self.I = max(0, self.I); self.R = max(0, self.R)
        self.history["S"].append(self.S)
        self.history["I"].append(self.I)
        self.history["R"].append(self.R)

    def run(self, days):
        for _ in range(days): self.step()
        return self.history

    def r0(self):
        return self.beta / self.gamma

    def peak_infected(self):
        return max(self.history["I"])

    def herd_immunity_threshold(self):
        return 1 - 1/self.r0()

class SEIR(SIR):
    def __init__(self, pop, infected=1, beta=0.3, gamma=0.1, sigma=0.2):
        super().__init__(pop, infected, beta, gamma)
        self.E = 0
        self.sigma = sigma
        self.history["E"] = [0]

    def step(self, dt=1):
        dS = -self.beta * self.S * self.I / self.N * dt
        dE = (self.beta * self.S * self.I / self.N - self.sigma * self.E) * dt
        dI = (self.sigma * self.E - self.gamma * self.I) * dt
        dR = self.gamma * self.I * dt
        self.S += dS; self.E += dE; self.I += dI; self.R += dR
        for attr in ("S","E","I","R"):
            setattr(self, attr, max(0, getattr(self, attr)))
        for attr in ("S","E","I","R"):
            self.history[attr].append(getattr(self, attr))

def summary(model):
    h = model.history
    return {
        "R0": round(model.r0(), 2),
        "peak_infected": round(model.peak_infected()),
        "total_infected": round(h["R"][-1]),
        "herd_immunity": f"{model.herd_immunity_threshold()*100:.1f}%",
        "days": len(h["S"]) - 1,
    }

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Epidemic simulation")
    p.add_argument("-p", "--pop", type=int, default=10000)
    p.add_argument("-b", "--beta", type=float, default=0.3)
    p.add_argument("-g", "--gamma", type=float, default=0.1)
    p.add_argument("-d", "--days", type=int, default=200)
    args = p.parse_args()
    m = SIR(args.pop, beta=args.beta, gamma=args.gamma)
    m.run(args.days)
    for k, v in summary(m).items():
        print(f"{k}: {v}")
