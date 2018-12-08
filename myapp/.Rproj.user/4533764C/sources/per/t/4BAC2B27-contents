library(shiny)
library(shinydashboard)
library(DT)
library(leaflet)
library(plotly)
library(tidyr)
library(shinyjs)
source("global.R", encoding = "utf-8")
library(reticulate)
source_python("cems_api.py")

# ui ----------------------------------------------------------------------
ui <- dashboardPage(skin = "green",
  dashboardHeader(title = span("AQ  Doctor", style="font-family:Microsoft JhengHei; font-size:25px; font-weight:bold")),
  dashboardSidebar(sidebarMenu(
    menuItem(span("CEMS",style="font-family:Microsoft JhengHei; font-size:18px"), tabName = "cems", icon = icon("industry"), startExpanded = TRUE, 
             menuSubItem(span("CEMS 資料品質",style="font-family:Microsoft JhengHei; font-size:16px"), tabName = "subitem1"),
             menuSubItem(span("CEMS 即時追蹤",style="font-family:Microsoft JhengHei; font-size:16px"), tabName = "subitem2")),
    menuItem(span("Airbox 選址推薦",style="font-family:Microsoft JhengHei; font-size:18px"), tabName = "airbox", icon = icon("map")),
    menuItem(span("Airbox 異常追蹤",style="font-family:Microsoft JhengHei; font-size:18px"), tabName = "illegal", icon = icon("search-plus"))
  )),
  dashboardBody(
    tabItems(
    # Second content
    tabItem(tabName = "airbox",  
            column(width = 9, box(width = NULL, solidHeader = TRUE, leafletOutput("pm25_map", height = 850))), 
            column(width = 3, box(width = NULL, selectInput("type", "工廠選擇", choices = cf_dCols)))
            ),
    
    # Third content
    tabItem(tabName = "illegal", tags$img(height = 720, width = 1280,src = "illegal.png")),
    
    # First sub-content 
    tabItem(tabName = "subitem1",
            fluidRow(tabBox(
        title = "CEMS 資料品質", 
        # The id lets us use input$tabset1 on the server to find the current tab
        id = "tabset1", height = "850px", width = "12",
        tabPanel("SOx", DT::dataTableOutput("cems_SOX")),
        tabPanel("NOx", DT::dataTableOutput("cems_NOX"))
      ))),
  
    tabItem("subitem2", selectInput("select", h3("選擇代碼"), 
                                    choices = cems_metadata$cno, selected = 1),
            box(title = "SOx", status = "success", solidHeader = TRUE,
                collapsible = TRUE, height = "400px", width = "12",
                tags$img(height = 340, width = 1180,src = "E5600056_so.png")),
            box(title = "NOx", status = "success", solidHeader = TRUE,
                collapsible = TRUE, height = "400px", width = "12",
                tags$img(height = 340, width = 1180,src = "E5600056_no.png"))
            ))
))

# server ------------------------------------------------------------------
server <- function(input, output) {
  # CEMS table
  output$tabset1Selected <- output$cems_SOX <- DT::renderDataTable({
    so_data
  },options = list(searching = FALSE, pageLength = 15
  ),
  callback=JS(
    'table.on("click.dt", "tr", function() {

    var x = document.getElementsByTagName("a")
    for (i = 0; i < x.length; i++) { 
        if (x[i].getAttribute("data-value")=="subitem2") {
        button = x[i]
        button.click()
        }
    }
    
    })'
  ))
  
  output$tabset1Selected <- output$cems_NOX <- DT::renderDataTable({
    no_data
  },options = list(searching = FALSE, pageLength = 15
  ),
  callback=JS(
    'table.on("click.dt", "tr", function() {
    
    var x = document.getElementsByTagName("a")
    for (i = 0; i < x.length; i++) { 
    if (x[i].getAttribute("data-value")=="subitem2") {
    button = x[i]
    button.click()
    }
    }
    
})'
  ))
  # CEMS Line chart prepare
  output$selected_var <- renderText({
    paste("You have selected", input$select)
  })
  SOInput <- reactive({
    SO_table <- instant_24(input$select) %>% subset(item == '922')
    SO_table$polno <- as.factor(unlist(SO_table$polno))
    SO_table$m_time <-  as.POSIXct(SO_table$m_time, format="%Y/%m/%d %H:%M")
  })
  
  # CEMS(Sox、Nox plot)
  output$SOplot <- renderPlotly({
    SO_ggplot<-ggplot(SOInput(), aes(x = m_time, y = m_val, color=polno)) + 
      geom_point() +
      geom_line()+
      theme_bw()+
      labs(y="ppm")+
      scale_x_datetime(date_labels="%m/%d %H:%M:%S")
    SO_linechart <- ggplotly(SO_ggplot)
  })
  
  NOInput <- reactive({
    NO_table <- instant_24(input$select) %>% subset(item == '923')
    NO_table$polno <- as.factor(unlist(NO_table$polno))
    NO_table$m_time <-  as.POSIXct(NO_table$m_time, format="%Y/%m/%d %H:%M")
  })
  
  output$Noplot <- renderPlotly({
    NO_ggplot<-ggplot(NOInput(), aes(x = m_time, y = m_val, color=polno)) + 
      geom_point() +
      geom_line()+
      theme_bw()+
      labs(y="ppm")+
      scale_x_datetime(date_labels="%m/%d %H:%M:%S")
    NO_linechart <- ggplotly(NO_ggplot)
  })
  
  # Initialization map  
  output$pm25_map <- renderLeaflet({pm25_map %>%
      addMinicharts(cems_factory$longitude, cems_factory$latitude, type = 'bar',layerId = cems_factory$towncode)})
  
  observe({
    cf_data <- cems_factory[, input$type]
    leafletProxy("pm25_map") %>%
      updateMinicharts(layerId = cems_factory$towncode, chartdata = cf_data, type = 'bar')
  })
}

shinyApp(ui, server)
