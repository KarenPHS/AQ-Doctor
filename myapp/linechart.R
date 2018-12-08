library(plotly)
library(dplyr)
library(shiny)
library(scales)
SOurce_python("cems_api.py")
SO_table <- instant_24("E5600850") %>% subset(item == '922')
NO_table <- instant_24("E5600850") %>% subset(item == '923')


SO_table$polno <- as.factor(unlist(SO_table$polno))
SO_table$m_time <-  as.POSIXct(SO_table$m_time, format="%Y/%m/%d %H:%M")
SO_ggplot<-ggplot(SO_table, aes(x = m_time, y = m_val,color=polno)) + 
  geom_point() +
  geom_line()+
  theme_bw()+
  labs(y="ppm")+
  scale_x_datetime(date_labels="%m/%d %H:%M:%S")


SO_ggplot

