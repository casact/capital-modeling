# make sure you run prefob and basic_example_script first!

ex070 = {}

## Ch 070
# Calculation of loss shares by layer.
bit = port.density_df.query('p_total > 0 or loss==0').filter(regex='p_total|S|exeqa|exi_xgta_X')
bit['dx'] = -bit.exeqa_total.diff(-1).fillna(0)
bit['a1S'] = bit.exi_xgta_X1 * bit.S
bit['a2S'] = bit.exi_xgta_X2 * bit.S
bit['a3S'] = bit.exi_xgta_X3 * bit.S
bit = bit[['exeqa_X1', 'exeqa_X2', 'exeqa_X3', 'exeqa_total',
          'p_total', 'S', 'dx', 'a1S', 'a2S', 'a3S']]
ep = (bit * bit[['p_total']].values).sum(0)
ep2 = (bit * bit[['dx']].values).sum(0)

# nan is hidden
ep['p_total'] = ep['S'] = ep['dx'] = np.nan
ep2['p_total'] = ep2['S'] = ep2['dx'] = np.nan
ep.iloc[-3:] = ep2.iloc[-3:]
bit.loc['$L=\\mathsf E_p$'] = ep

bit.index = list(range(8)) + [bit.index[-1]]
bit.index.name = '$k$'
bit.columns = ['Unit A $X^1$', 'Unit B $X^2$', 'Unit C $X^3$', 'Total $X$', '$p$', '$S$', '$\\Delta X$'
              , '$\\alpha^1 S$', '$\\alpha^2 S$', '$\\alpha^3 S$']
ex070['tbl-alpha'] = nGT(bit, tikz_scale=0.75, max_table_inch_width=10)


# Calculation of premium shares by layer.
port.calibrate_distortions(Ps=[1], COCs=[.15])
port.apply_distortion(port.dists['wang'])

bitg = port.augmented_df.query('p_total > 0 or loss==0').filter(regex='gp_total|gS|exeqa|exi_xgtag_X')
bitg['dx'] = -bitg.exeqa_total.diff(-1).fillna(0)
bitg['a1S'] = bitg.exi_xgtag_X1 * bitg.gS
bitg['a2S'] = bitg.exi_xgtag_X2 * bitg.gS
bitg['a3S'] = bitg.exi_xgtag_X3 * bitg.gS
bitg = bitg[['exeqa_X1', 'exeqa_X2', 'exeqa_X3', 'exeqa_total',
          'gp_total', 'gS', 'dx', 'a1S', 'a2S', 'a3S']]
eq = (bitg * bitg[['gp_total']].values).sum(0)
eq2 = (bitg * bitg[['dx']].values).sum(0)

# nan is hidden
eq['gp_total'] = eq['gS'] = eq['dx'] = np.nan
eq2['gp_total'] = eq2['gS'] = eq2['dx'] = np.nan
eq.iloc[-3:] = eq2.iloc[-3:]
ep.iloc[-3:] = np.nan
bitg.loc['$L=\\mathsf E_p$'] = ep
bitg.loc['$P=\\mathsf E_p$'] = eq
bitg.loc['$M=P-L$'] = eq - ep

bitg.index = list(range(8)) + list(bitg.index[-3:])
bitg.index.name = '$k$'
bitg.columns = ['Unit A $X^1$', 'Unit B $X^2$', 'Unit C $X^3$', 'Total $X$', '$q$', '$gS$', '$\\Delta X$'
               , '$\\beta^1 S$', '$\\beta^2 S$', '$\\beta^3 S$']
ex070['tbl-beta'] = nGT(bitg, tikz_scale=0.75)


# Allocation of capital
xdx = bit.iloc[:-1, [3,6]]
margins = bitg.iloc[:-3, -3:] - bit.iloc[:-1, -3:].values
margins.columns = [f'$M^{i}$' for i in [1,2,3]]
bitq = port.augmented_df.query('p_total > 0 or loss == 0').filter(regex='Q_X').fillna(0)
# bitq['dx'] =  xdx.iloc[:, [1]]
Q = (-bitq.diff(-1) /  xdx.iloc[:, [1]].values).fillna(0)
Q.columns = [f'$Q^{i}$' for i in [1,2,3]]
Q.index = margins.index
bit_qalloc = pd.concat((xdx, margins, Q), axis=1)
# add totals
# bit_qalloc[[f'$\\iota^{i}$' for i in [1,2,3]]] = bit_qalloc.iloc[:, 2:5].values / bit_qalloc.iloc[:, 5:8].values
bit_qalloc['$\\iota$'] = bit_qalloc.iloc[:, 2:3].values / bit_qalloc.iloc[:, 5:6].values
bit_qalloc['$\\delta$'] = bit_qalloc.iloc[:, 2:3].values / (bit_qalloc.iloc[:, 2:3].values + bit_qalloc.iloc[:, 5:6].values)

q = bitg.iloc[:-3, [4]].values
dx = bitg.iloc[:-3, [6]].values
eq = (bit_qalloc * q).sum(0)
eq2 = (bit_qalloc * dx).sum(0)
eq2.iloc[[0,1,-2,-1]] = np.nan
bit_qalloc.loc['$\\mathsf E_q$'] = eq2 # pd.concat((eq, eq2), axis=1).T
iota = eq2.iloc[2:5].values / eq2.iloc[5:8]
bit_qalloc.loc['$\\iota$'] = iota
bit_qalloc.loc['$\\iota$', '$\\iota$'] = eq2.iloc[2:5].sum() / eq2.iloc[5:8].sum()
ex070['tbl-q-alloc'] = nGT(bit_qalloc, tikz_scale=0.75)


ans = port.analyze_distortions(p=1, add_comps=False)
comp = ans.comp_df.loc[['Dist ccoc', 'Dist wang']].iloc[[5,2,6,13,10,14]].reset_index(drop=False)
comp['Method'] = [f'CCoC, {port.dists["ccoc"].shape:.3f}', '', '', f'Wang, {port.dists["wang"].shape:.3f}', '', '']
comp['stat'] = ['Capital $Q$', 'Margin $M$', 'Return $\\iota$'] * 2
comp.columns = ['Distortion', 'Metric', 'Unit A', 'Unit B', 'Unit C', 'Portfolio']
comp = comp.iloc[[3,4,5,0,1,2]]
comp = comp.set_index(['Distortion', 'Metric'])
comp.iloc[[2,5]] = comp.iloc[[2,5]].map(lambda x: f'{x:.1%}')
ex070['tbl-wang-isa-alloc'] = fGT(comp, aligners={c: 'r' for c in comp.columns}) #, show_index=False) # , ratio_cols='Unit|Port')



bodoff = port.density_df.query('p_total > 0 or loss==0').filter(regex='p_total|S|exeqa|exi_xgta_X')
bodoff['dx'] = -bodoff.exeqa_total.diff(-1).fillna(0)
bodoff['a1S'] = bodoff.exi_xgta_X1 * bodoff['dx']
bodoff['a2S'] = bodoff.exi_xgta_X2 * bodoff['dx']
bodoff['a3S'] = bodoff.exi_xgta_X3 * bodoff['dx']
bodoff = bodoff[['exeqa_X1', 'exeqa_X2', 'exeqa_X3', 'exeqa_total',
          'p_total', 'S', 'dx', 'a1S', 'a2S', 'a3S']]
ep = (bodoff * bodoff[['p_total']].values).sum(0)
ep2 = (bodoff ).sum(0)

# nan is hidden
ep['p_total'] = ep['S'] = ep['dx'] = np.nan
ep2['p_total'] = ep2['S'] = ep2['dx'] = np.nan
ep.iloc[-3:] = ep2.iloc[-3:]
bodoff.loc['Total'] = ep

bodoff.index = list(range(8)) + [bodoff.index[-1]]
bodoff.index.name = '$k$'
bodoff.columns = ['Unit A $X^1$', 'Unit B $X^2$', 'Unit C $X^3$', 'Total $X$', '$p$', '$S$', '$\\Delta X$'
              , '$\\alpha^1\\Delta X$', '$\\alpha^2\\Delta X$', '$\\alpha^3\\Delta X$']
bodoff['$\\sum\\alpha^i\\Delta X$'] = bodoff.iloc[:, -3:].sum(1)
bodoff = bodoff.iloc[:, 3:]
ex070['tbl-bodoff'] = fGT(bodoff)
