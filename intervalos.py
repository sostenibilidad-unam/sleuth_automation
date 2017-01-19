import pandas

widths = [7,8,8,8,8,8,8,8,8,8,8,8,8,8,5,5,5,5,5]
df = pandas.read_fwf("control_stats.log", skiprows = 1, widths = widths)
primeros10 = df.sort_values(by = 'Leesalee', ascending = False)[:10]

DiffMax = primeros10['Diff'].max()
BrdMax = primeros10['Brd'].max()
SprdMax = primeros10['Sprd'].max()
SlpMax = primeros10['Slp'].max()
RGMax = primeros10['RG'].max()

DiffMin = primeros10['Diff'].min()
BrdMin = primeros10['Brd'].min()
SprdMin = primeros10['Sprd'].min()
SlpMin = primeros10['Slp'].min()
RGMin = primeros10['RG'].min()

print "Diff: " + str(DiffMin) + ", " + str(DiffMax)
print "Brd: " + str(BrdMin) + ", " + str(BrdMax)
print "Sprd: " + str(SprdMin) + ", " + str(SprdMax) 
print "Slp: " + str(SlpMin) + ", " + str(SlpMax) 
print "RG: " + str(RGMin) + ", " + str(RGMax)  

