ext <- "data/NOX-2020-ext.csv"   # TSV
df <- read.delim(ext, sep="\t", stringsAsFactors=FALSE, check.names=FALSE)

# 1) NOX-2020.csv (sin nombres de estado/condado/método)
drop <- c("State.Name","County.Name","Method.Name")
keep <- setdiff(colnames(df), drop)
write.csv(df[keep], file="data/NOX-2020.csv", row.names=FALSE, na="")

# 2) states.csv
states <- unique(df[c("State.Code","State.Name")])
states <- states[order(states$State.Code, states$State.Name), ]
write.csv(states, file="data/states.csv", row.names=FALSE, na="")

# 3) counties.csv
counties <- unique(df[c("State.Code","County.Code","County.Name")])
counties <- counties[order(counties$State.Code, counties$County.Code, counties$County.Name), ]
write.csv(counties, file="data/counties.csv", row.names=FALSE, na="")

# 4) methods.csv
methods <- unique(df[c("Method.Code","Method.Name")])
methods <- methods[order(methods$Method.Code, methods$Method.Name), ]
write.csv(methods, file="data/methods.csv", row.names=FALSE, na="")

# Checks rápidos a consola
cat("Estados únicos:", length(unique(states$State.Code)), "\n")
cat("Condados únicos:", nrow(unique(counties[c("State.Code","County.Code")])), "\n")
cat("Métodos únicos:", length(unique(methods$Method.Code)), "\n")
cat("Filas NOX-2020.csv:", nrow(read.csv("data/NOX-2020.csv")), "\n")
