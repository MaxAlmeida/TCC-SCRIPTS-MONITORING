import workload as app

app.run_bw_mem(10)
app.run_bw_mem(15)
app.run_bw_mem(30)
app.run_bw_mem(60)
app.run_bw_mem(120)

app.run_gzip(10)
app.run_gzip(15)
app.run_gzip(30)

app.run_make(10)
app.run_make(15)
app.run_make(30)

