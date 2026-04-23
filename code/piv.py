mydata = 2

mydata = mydata.groupby('year')[["columnA", "columnB", "columnC"]].mean()
mydata = mydata.reset_index()
mydata.loc[mydata.columnA > 0, "columnC"] = mydata["columnB"] / mydata["columnA"]


mydata = (mydata                                                                                                                                                                                                       
.groupby('year')                                                                                                                                                                                                     
[["columnA", "columnB", "columnC"]]                                                                                                                                                                                  
.mean()                                                                                                                                                                                                              
.reset_index()                                                
)

mask = mydata.columnA > 0
mydata.loc[mask, "columnC"] = (
mydata["columnB"]
/ mydata["columnA"]
)




