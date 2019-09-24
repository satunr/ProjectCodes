from pygurobi import *

# tested with Python 3.5.2 & Gurobi 7.0.1

mines = range(3+1)
years = range(4+1)

Royalties = [5e6, 4e6, 4e6, 5e6]
ExtractLimit = [2e6, 2.5e6, 1.3e6, 3e6]
OreQuality  = [1, .7, 1.5, .5]
BlendedQuality = [0.9, 0.8, 1.2, 0.6, 1.0]
discount = [(1/(1+1/10.0)) ** year for year in years]

mines_limit = 3
sell_price = 10

model = Model('Mining')

out = model.addVars(mines, years, name="output")
quan = model.addVars(years, name="quantity")
work = model.addVars(mines, years, vtype=GRB.BINARY, name="working")
open = model.addVars(mines, years, vtype=GRB.BINARY, name="open")