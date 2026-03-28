#!/usr/bin/env python3
"""epidemic_sim - SIR epidemic model simulation."""
import argparse, json

def sir_model(population, infected, beta, gamma, days):
    S, I, R = population - infected, infected, 0
    history = [{"day": 0, "S": S, "I": I, "R": R}]
    for day in range(1, days + 1):
        new_infected = beta * S * I / population
        new_recovered = gamma * I
        S -= new_infected; I += new_infected - new_recovered; R += new_recovered
        S, I, R = max(0, S), max(0, I), max(0, R)
        history.append({"day": day, "S": round(S), "I": round(I), "R": round(R)})
    return history

def main():
    p = argparse.ArgumentParser(description="SIR epidemic simulation")
    p.add_argument("-N", "--population", type=int, default=10000)
    p.add_argument("-I", "--infected", type=int, default=10)
    p.add_argument("-b", "--beta", type=float, default=0.3, help="Transmission rate")
    p.add_argument("-g", "--gamma", type=float, default=0.1, help="Recovery rate")
    p.add_argument("-d", "--days", type=int, default=100)
    p.add_argument("--json", action="store_true")
    p.add_argument("--chart", action="store_true")
    args = p.parse_args()
    r0 = args.beta / args.gamma
    print(f"R0 = {r0:.2f} ({'epidemic' if r0 > 1 else 'contained'})")
    history = sir_model(args.population, args.infected, args.beta, args.gamma, args.days)
    if args.json:
        print(json.dumps(history, indent=2))
    elif args.chart:
        peak = max(history, key=lambda h: h["I"])
        print(f"Peak: day {peak['day']}, {peak['I']} infected")
        ticks = "▁▂▃▄▅▆▇█"
        mx = max(h["I"] for h in history)
        spark = "".join(ticks[min(int(h["I"]/max(1,mx)*7), 7)] for h in history[::max(1,len(history)//60)])
        print(f"Infections: {spark}")
    else:
        for h in history[::max(1, len(history)//20)]:
            print(f"Day {h['day']:3d}: S={h['S']:6d} I={h['I']:6d} R={h['R']:6d}")

if __name__ == "__main__":
    main()
