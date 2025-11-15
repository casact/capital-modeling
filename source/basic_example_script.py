r"""
Everything for the basic example. Set up and run as follows in qmd file:

    %run \s\telos\capitalmodeling\tma1\basic_example_script.py
    for i, (k, v) in enumerate(exhibits.items()):
        if i < 0:
            continue
        print(i, k)
        display(v)

MUST RUN prefob FIRST!
"""

exhibits = {}



# reinsurance version
wgs_re = pd.DataFrame(
    {
        'X1': [36, 40, 28, 22, 33, 32, 31, 45, 25, 25],
        'X2': [ 0, 0, 0, 0, 7, 8, 9, 10, 40, 40],
        'X3': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 35],
        'p_total': 1 / 10
    }
)


gcn_namer = {'X2': 'X2 net', 'X3': 'X2 ceded', 'X': 'X2', 'X4': 'X2'}


def gcn(df):
    bit = df.loc[['X2', 'X3']]
    df.loc['X', :] = bit.sum(0)
    df.loc['X', 'LR'] = df.loc['X', 'L'] / df.loc['X', 'P']
    df.loc['X', 'PQ'] = df.loc['X', 'P'] / df.loc['X', 'Q']
    df.loc['X', 'COC'] = df.loc['X', 'M'] / df.loc['X', 'Q']
    df = df.rename(index=gcn_namer)
    df = df.sort_index()
    return df


# ==========================================================================
# 020 basic example setup
# ==========================================================================
# port object and calibrate distortions
# losses
wgs = pd.DataFrame(
    {
        'X1': [15, 15, 5, 7, 13, 5, 15, 26, 17, 16],
        'X2': [  7, 13, 20, 33, 20, 27, 16, 19, 8, 20],
        'X3': [  0, 0, 11, 0, 7, 8, 9, 10, 40, 64],
        'p_total': 1 / 10
    }
)
port = Portfolio.create_from_sample('ToyCo', wgs, bs=1, log2=8)
port.calibrate_distortions(Ps=[1], COCs=[.15])
ans = port.price(1, allocation='linear')


# make and display basic stats
# | fig-cap: "InsCo loss probability mass function by unit."
wgs_ = wgs.copy().drop(columns='p_total')
wgs_['total'] = wgs.drop(columns='p_total').sum(1)
wgs_.index = range(1, len(wgs) + 1)
wgs_.index.name = "Event $j$"
wgs2 = wgs_.copy()
wgs2.loc['EX', :] = wgs_.mean(0)
wgs2.loc['EX2', :] = (wgs_**2).mean(0)
wgs2.loc['Var', :] = wgs2.loc['EX2', :] - wgs2.loc['EX', :]**2
wgs2.loc['CV', :] = wgs2.loc['Var', :]**.5 / wgs2.loc['EX', :]
wgs2 = wgs2.drop(index=['EX2', 'Var'])
wgs2.columns = ['Unit A $X^1_j$', 'Unit B $X^2_j$', 'Unit C $X^3_j$', 'Total $X_j$']
# wgs2 = wgs2.drop(index = ['EX2', 'Var']).rename(columns=gcn_namer)
plan_premium = (13.9, 18.7, 19.6, 52.2)
wgs2.loc['Plan Prem', :] = plan_premium
assert plan_premium[-1] == sum(plan_premium[:-1])
exhibits['tbl-dupe-x'] = fGT(wgs2, unbreakable='Event $j$')  # .iloc[:-3])


# ==========================================================================
# 030 None
# ==========================================================================


# ==========================================================================
# 040 None
# ==========================================================================


# Table: Industry Standard Approach to allocation. {#tbl-isa-alloc}
df = wgs2.copy()
isa = df.loc[['EX', 10]]
nu = 1 / 1.15
delta = 1 - nu
isa.loc['Q'] = nu * (isa.loc[10] - isa.loc['EX'])
isa.loc['P'] = nu * isa.loc['EX'] + delta * isa.loc[10]
isa.loc['M'] = isa.loc['P'] - isa.loc['EX']
isa.loc['aM'] = isa.loc['M'] / isa.loc['M'].iloc[:-1].sum()
isa.loc['i'] = isa.loc['M'] / isa.loc['Q']
isa.index = [r'$L=\mathsf E[X]$',
             r'$a=\mathsf{TVaR}$',
             r'$Q=\nu\mathsf{XTVaR}$',
             '$P$',
             '$M=P-L$',
             'Allocation of $M$',
             r'$\iota=M/Q$']
isa.index.name = 'Variable'
exhibits['tbl-isa-alloc'] = fGT(isa)

# outcomes, prob, loss by unit, total, expectation, plan premium
# | fig-cap: "InsCo loss probability distribution by unit with duplicate $X$ averaged out and zero row inserted."
bit = port.density_df.query('p_total > 0').filter(regex='exeqa_X|loss|p_total').copy()
bit.columns = ['Portfolio $X_k$', '$p$', 'Unit A $X^1_k$', 'Unit B $X^2_k$', 'Unit C $X^3_k$']
bit.index = range(1, 8)
bit.loc[0, :] = [0, 0, 0, 0, 0]
bit = bit.sort_index()
bit.index.name = '$k$'
bit = bit.iloc[:, [1, 2, 3, 4, 0]]
bit2 = bit.copy()
bit2.loc['$\\mathsf E[X]$', :] = (bit.iloc[:, 1:] * bit.iloc[:, [0]].values).sum()
bit2.iloc[-1, 0] = ''
bit2.loc['Plan Prem', :] = 0
bit2.iloc[-1, 1:] = wgs2.loc['Plan Prem'].values
bit2.iloc[-1, 0] = ''
exhibits['tbl-abc-x'] = fGT(bit2, aligners='l' + 'r' * (bit2.shape[1] - 1))


# collapse down to unique events and do pricing
# | fig-cap: "InsCo layer loss details."
bit3 = bit.copy()
bit3.columns = ['$p$', 'Unit A $X^1_k$', 'Unit B $X^2_k$', 'Unit C $X^3_k$', 'Portfolio $X_k$']
bit3.index.name = '$k$'
bit3.loc[0, :] = [0, 0, 0, 0, 0]
bit3 = bit3.sort_index()
bit3['Layer size $\\Delta X_k$'] = np.diff(bit3.iloc[:, 4], append=100)
bit3['Exceedance Pr $S_k$'] = bit3.iloc[:, 0][::-1].cumsum()[::-1].shift(-1, fill_value=0)
exhibits['tbl-x-collapsed'] = fGT(bit3)


# | fig-cap: "Pricing the portfolio with CCoC distorted $g(S)$."
g = Distortion.ccoc(.15 / 1.15)
bit4 = bit3.copy().iloc[:, [0, 4, 5, 6]]
bit4['Distorted $g(S)$'] = g.g(bit4.iloc[:, -1])
bit4['$S\\Delta X$'] = bit4.iloc[:, 2] * bit4.iloc[:, 3]
bit4['$g(S)\\Delta X$'] = bit4.iloc[:, 2] * bit4.iloc[:, 4]
bit4.loc['Sum'] = bit4.sum()
bit4.iloc[-1, [1, 3, 4]] = np.nan
exhibits['tbl-ccoc-1'] = fGT(bit4.fillna(''), aligners='l' + 'r' * 6)


# | Pricing the portfolio with CCoC distorted probabilities $q$.
bit5 = bit4.copy().iloc[:, [0, 1, 2, 3]]
bit5['$pX$'] = bit5.iloc[:, 0] * bit5.iloc[:, 1]
bit5['Distorted $q$'] = -np.diff(bit4['Distorted $g(S)$'], prepend=1)
bit5['$qX$'] = bit5.iloc[:, -1] * bit5.iloc[:, 1]
bit5['$qX$'].iloc[-1] = bit5['$qX$'].iloc[:-1].sum()
bit5['$Z=q/p$'] = (
    bit5.iloc[:, -2].astype(float)
    .div(bit5.iloc[:, 0].astype(float))
)
exhibits['tbl-ccoc-qx'] = fGT(bit5)

# distortion calibration
# | Distortion functions calibrated to portfolio price $\rho(X)=53.565$.
port.calibrate_distortions(Ps=[1.], LRs=[46.6 / 53.565])
table = r'''
| **Distortion** | **Formula**                  | **Parameter**    |
|:---------------|:-----------------------------|:-----------------|
| CCoC           | $\nu s+\delta$               | $\iota={ccoc:.4f}$     |
| PH             | $s^\alpha$                   | $\alpha={ph:.4f}$  |
| Wang           | $\Phi(\Phi^{{-1}}(s)+\lambda)$ | $\lambda={wang:.4f}$ |
| Dual           | $1-(1-s)^m$                  | $m={dual:.4f}$  |
| TVaR           | $1\wedge s/(1-p)$            | $p={tvar:.4f}$       |
'''
c, w, p, d, t = port.distortion_df.param.values
table = table.format(ccoc=c, wang=w, ph=p, dual=d, tvar=t)
exhibits['tbl-the5dists'] = fGT(table)

# | label: fig-market
# | fig-cap: "Distorted exceedance ($g(s)$, left) and distorted probabilities ($q$, right) by distortion type."
# put formatter back
# pd.options.display.float_format = tff
fig, axs = plt.subplots(1, 2, figsize=(2 * 2.5, 2.5), constrained_layout=True, sharey=False)
ax0, ax1 = axs.flat
ps = np.linspace(0, 1, 1001)

colors = {k: f'C{i}' for i, k in enumerate(port.dists.keys())}

ax = ax0
for (k, v) in port.dists.items():
    ax.plot(ps, v.g(ps), lw=1, label=k, c=colors[k])
ax.set(aspect='equal', xlabel='$s$', ylabel='$g(s)$')
ax.legend(loc='lower right', fontsize='x-small')


ax = ax1
ps = np.linspace(0, 1, 101)
ps = ps[1:-1]
for (k, v) in port.dists.items():
    ax.plot(ps, list(map(v.g_prime, ps)), lw=1, label=k, c=colors[k])
ax.set(xlabel='$s$', ylabel="$g'(s)$")
ax.legend(loc='upper right', fontsize='x-small')
ax.text(0, 2.75, '*', c=colors['ccoc'])
ax.axhline(1, lw=0.25, c='k')
fig.savefig('img/fig-the5dists.svg')
plt.close(fig)
del fig

# tables of g(s), q, and z ---------------------------------------------------------
renamer = {'ccoc': 'CCoC',
           'ph': 'PH',
           'dual': 'Dual',
           'wang': 'Wang',
           'tvar': 'TVaR'}

# | fig-cap: "Distorted exceedance ($g(s)$) by distortion type."
df = bit3.iloc[:, [-1]].rename(columns={bit3.columns[-1]: '$S$'})
# cn = list(df.columns)
# cn[0] = '$S$'
# df.columns = cn
for k, v in port.dists.items():
    df[k] = v.g(df.iloc[:, 0])
exhibits['tbl-the5gs'] = f4GT(df.rename(columns=renamer))

# | fig-cap:   Distorted probabilities ($q$) by distortion type.
df2 = -df.diff( axis=0).iloc[1:].rename(columns={'$S$': '$p$'})
# cn = list(df2.columns)
# cn[0] = '$p$'
# df2.columns = cn
exhibits['tbl-the5qs'] = f4GT(df2.rename(columns=renamer))

# | fig-cap: "Radon-Nikodynm derivatives ($Z=q/p$) by distortion type."
df3 = (df2 / df2.iloc[:, [0]].values).rename(columns={'$S$': '$p$'})
# cn = list(df3.columns)
# cn[0] = '$p$'
# df2.columns = cn
exhibits['tbl-the5zs'] = f4GT(df3.rename(columns=renamer))


# | fig-cap: "Pricing the portfolio with Wang transformed probabilities $q$."
lhs = exhibits['tbl-abc-x'].raw_df.copy().iloc[:8]
rhs1 = exhibits['tbl-the5gs'].raw_df.copy()[['$S$', 'Wang']].rename(columns={'Wang': '$g(S)$'})
rhs2 = exhibits['tbl-the5qs'].raw_df.copy()[['Wang']].rename(columns={'Wang': '$q$'})
rhs3 = exhibits['tbl-the5zs'].raw_df.copy()[['Wang']].rename(columns={'Wang': '$Z$'})
combo = pd.concat((lhs, rhs1, rhs2, rhs3), axis=1).fillna(0)
L = combo.iloc[:, 1:5] * combo.iloc[:, [0]].values
L = L.sum()
P = combo.iloc[:, 1:5] * combo.iloc[:, [7]].values
P = P.sum()
combo2 = combo.copy()
combo2.loc['$L=\\mathsf E_p$', :] = ['', *L, '', '', '', '']
combo2.loc['$P=\\mathsf E_q$', :] = ['', *P, '', '', '', '']
combo2.loc['$M=P-L$', :] = ['', *(P - L), '', '', '', '']
combo2.loc['Prop of tot $M$', :] = ['', *((P - L) / (P - L).iloc[-1]), '', '', '', '']
exhibits['tbl-wang-alloc'] = fGT(combo2, aligners='l' + 'r' * (combo2.shape[1] - 1))



# ==========================================================================
# 060 Distortions
# ==========================================================================
# table 6.1 "$q$ values for $\mathsf{TVaR}_0=E[X]$, $\mathsf{TVaR}_1=\max(X)$ and the $\theta=0.87$ blend.
blend = port.density_df.query('p_total > 0 or loss == 0').filter(regex='^(p_total|S)$')
blend['TVaR 0 gS'] = blend.S
blend['TVaR 1 gS'] = Distortion.tvar(1).g(blend.S)
blend['blend gS'] = Distortion.bitvar(0, 1, 1 - 1/1.15).g(blend.S)

blend['TVaR 0'] = -blend['TVaR 0 gS'].diff(1).fillna(0)
blend['TVaR 1'] = -blend['TVaR 1 gS'].diff(1).fillna(0)
blend['Blend'] = -blend['blend gS'].diff(1).fillna(0)
blend.index = range(8)
blend.index.name = '$k$'
blend = blend[['p_total', 'S', 'TVaR 0', 'TVaR 1', 'Blend']]
blend.columns = ['$p$', '$S$', '$\\mathsf{TVaR}_0$', '$\\mathsf{TVaR}_1$', 'Blend']
exhibits['tbl-bi-tvar'] = fGT(blend)



# 6.2 Table 6.2
ans = port.analyze_distortions(p=1, add_comps=False)
ans.comp_df.columns = ['Unit A', 'Unit B', 'Unit C', 'Portfolio']
ans.comp_df.loc[('Plan', 'P'), :] = wgs2.loc['Plan Prem'].values
ans.comp_df.loc[('Plan', 'LR'), :] = (wgs2.loc['EX'] / wgs2.loc['Plan Prem']).values

ans = port.analyze_distortions(p=1, add_comps=False)
ans.comp_df.columns = ['Unit A', 'Unit B', 'Unit C', 'Portfolio']
ans.comp_df.loc[('Plan', 'P'), :] = wgs2.loc['Plan Prem'].values
ans.comp_df.loc[('Plan', 'LR'), :] = (wgs2.loc['EX'] / wgs2.loc['Plan Prem']).values
exh62 = pd.concat((ans.comp_df.xs('P', 0, 1).rename(index=lambda x: x.replace('Dist ', '')),
                   ans.comp_df.xs('LR', 0, 1).rename(index=lambda x: x.replace('Dist ', ''))),
                    keys=['Premium', 'Loss ratio'],
                    names=['Metric', 'View']).unstack(0)
exhibits['tbl-3units'] = fGT(exh62, vrule_widths=(1,0,0), ratio_cols='Loss')


#
rg = ans.comp_df.xs('LR', 0, 1).rename(index=lambda x: x.replace('Dist ', '')).T
rg['Cheapest'] = rg.apply(lambda x: x.idxmax(), axis=1)
ex63 = rg.iloc[:-1]
ex63.index.name = 'Unit'
ex63 = ex63[['ccoc', 'ph', 'wang', 'dual', 'tvar', 'Plan', 'Cheapest']]
exhibits['tbl-bestlr'] = fGT(ex63, ratio_cols='all')
