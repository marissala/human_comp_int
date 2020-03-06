#############################################################################
################### Assigment 1 - Make a graph in the App ###################
#############################################################################
# a) install packages "shiny" & "shinydashboard" - then press "Run App" (or just run all the code)
# b) Complete the output$testDataPlot1 with a plot within the brackets in the server code - done
# c) Create an additional page like the "Dashboard"-page - done
# d) Create a second plot to display on this additional page - done
# e) Create some text and headlines on both pages
# f) Create a "Select box" in the UI  - see: https://shiny.rstudio.com/gallery/select-box.html
# optional) Make the "Select box" interactive - so that it controls what is being plotted an axis in testDataPlot1 

pacman::p_load(shiny, shinydashboard)
library(shiny)
library(shinydashboard)
library(ggplot2)

ui <- dashboardPage(
  dashboardHeader(
    title = "Exercise 1"
  ),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName ="Dashboard_tab", icon = icon("tachometer-alt")),
      menuItem("How to level up", tabName = "New_tab")
    )
  ),
  
  dashboardBody(
    mainPanel(
      tabName = "Dashboard_tab",
      h1("helloes worlds")
    ),
    tabItems(
      tabItem(tabName = "Dashboard_tab",
              selectInput("selectInputIris", "Select data column",
                          choices = c("Sepal length" = "Sepal.Length",
                                      "Sepal width" = "Sepal.Width",
                                      "Petal length" = "Petal.Length",
                                      "Petal width" = "Petal.Width",
                                      "Species" = "Species")),
              plotOutput("testDataPlot1"),
              h2("whats up")),
      tabItem(tabName = "New_tab",
              h2("not much man"),
              plotOutput("testDataPlot2"))
      )
    
  )#body
  
)#ui end


server <- function(input, output) {
  appData = iris #our testData taken from iris-dataset
  
  output$testDataPlot1 <- renderPlot({
    #b) Write a plot here - that is to be displayed in the app
    ggplot(appData, aes_string(input$selectInputIris, "Sepal.Width")) +
      geom_point()
  })
  
  output$testDataPlot2 <- renderPlot({
    ggplot(appData, aes(Petal.Length, Petal.Width)) +
      geom_line()
  }
  
  )
  
}#server end


shinyApp(ui, server) #Run app


########## HINTS ###########
# b) Use ggplot within  "renderPlot([ #HERE ])"
# c) Create another menuItem (the ID/tabName must be unique)
# d) Use 'plotOutput()' and 'output$...'
# d) Repeat what you already have
# e) use play text within "" or h1() or h2() etc.
# f) Read the link
# optional: You may need to use aes_string() in ggplot - because the 'input$selectBoxIrisGraph' probably is a string.