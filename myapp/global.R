library(leaflet.minicharts)
library(htmltools)
library(leaflet)
library(dplyr)
library(rgdal)
library(data.table)
#call python file 
library(scales)
library(reticulate)
source_python("cems_api.py")

#cems-table related
so_data <- Sox() %>% data.table()
no_data <- Nox() %>% data.table()

cems_metadata <- read.csv('data/cems_metadata.csv', fileEncoding =  "utf8")
choice.cno <- list(cems_metadata$cno)

# map-related
pm25_data <- readOGR('data/pm25/pm25_mean.shp', use_iconv = TRUE, encoding = "UTF-8")
cemsFactory_data <- read.csv('data/cems_factory.csv', fileEncoding =  "utf8")

cems_factory <- cemsFactory_data %>% select("一般工廠", "監督工廠", longitude, latitude, towncode)
cf_dCols <- names(cems_factory)[1:2]

labels <- sprintf(
  "<strong>%s</strong><br/>%g μg/m3<sup>2</sup>",
  paste(pm25_data$countyname, pm25_data$townname), pm25_data$pm25
) %>% lapply(htmltools::HTML)
bins <- c(0, 11,23,35,41,47,53,58,64,70,Inf)
mycols<-c('#9dff9c','#31ff00','#31cf00','#ffff00','#ffcf00','#ff9a00','#fe6464','#fe0000','#990100','#ce30ff')
pal <- colorBin(mycols, domain = pm25_data$pm25, bins = bins)

pm25_map <- leaflet(pm25_data) %>%
  addTiles("OpenStreetMap_DE") %>%
  setView(lng = 121.084560, lat = 23.8, zoom = 8)%>%
  addPolygons(data = pm25_data,
              fillColor = ~pal(pm25),
              weight = 2,
              opacity = 1,
              color = "white",
              dashArray = "3",
              fillOpacity = 0.7,
              highlight = highlightOptions(
                weight = 5,
                color = "#666",
                dashArray = "",
                fillOpacity = 0.7,
                bringToFront = TRUE),
              label = labels,
              labelOptions = labelOptions(
                style = list("font-weight" = "normal", padding = "3px 8px"),
                textsize = "15px",
                direction = "auto"))%>%
  addLegend(pal = pal, values = ~density, opacity = 0.7, title = NULL,
            position = "bottomright")


