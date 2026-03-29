from epidemic_sim import SIR, SEIR, summary
m = SIR(10000, 10, beta=0.3, gamma=0.1)
m.run(200)
s = summary(m)
assert s["R0"] == 3.0
assert s["peak_infected"] > 10
assert s["total_infected"] > 100
m2 = SEIR(10000, 10, beta=0.3, gamma=0.1, sigma=0.2)
m2.run(200)
assert m2.peak_infected() > 0
print("Epidemic sim tests passed")