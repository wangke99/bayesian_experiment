from pandas import DataFrame
import pandas as pd
import pymc as pm
import numpy as np
import matplotlib.pyplot as plt


raw = pd.read_csv('data/cleaned_sp500.txt', sep=',', encoding='utf-8')

data = raw[raw['ticker'] == 'GOOG'].reset_index()

mu = np.mean(data['daily_log'])
sigma = np.std(data['daily_log'])

mu1 = pm.Normal('mu1', mu=mu, tau = 1.0/(sigma**2))
mu2 = pm.Normal('mu2', mu=mu, tau=1.0/(sigma**2))

tau = pm.DiscreteUniform("tau", lower=0, upper=len(data['daily_log']))

@pm.deterministic
def mu_(tau = tau, mu1 = mu1, mu2 = mu2):
    out = np.zeros(len(data['daily_log']))
    out[:tau] = mu1
    out[tau:] = mu2
    return out

observation = pm.Normal('obs', mu_, value=data['daily_log'], observed=True)

model = pm.Model([observation, tau, mu1, mu2])

mcmc = pm.MCMC(model)
mcmc.sample(40000, 1000, 1)

mu1_sample = mcmc.trace('mu1')[:]
mu2_sample = mcmc.trace('mu2')[:]
tau_sample = mcmc.trace('tau')[:]

print mu1_sample
print mu2_sample
print tau_sample

#tau_his = np.histogram(tau_sample, bins=range(len(data['daily_log'])+1))

#print tau_his
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(mu1_sample, 50)
ax.hist(mu2_sample, 50)
plt.savefig('data/explore/GOOG-mu.png')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(tau_sample, len(data['daily_log']))
plt.savefig('data/explore/GOOG-tau.png')

quit()

