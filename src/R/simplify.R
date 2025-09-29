data <- read.csv("data/hourly_42602_2020.csv", sep=",")
write.table(
  data[, c("State.Code","County.Code","Site.Num",
           "Latitude","Longitude","Date.Local","Time.Local",
           "Sample.Measurement","Method.Type","Method.Code",
           "Method.Name","State.Name","County.Name")],
  file = "data/NOX-2020-ext.csv", sep = "\t",
  na = "", row.names = FALSE
)
