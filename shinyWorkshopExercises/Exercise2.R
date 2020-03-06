#############################################################################
#################### Assigment 2 - A button and a number ####################
#############################################################################
# a) Make the button "Click me!" print a number in the console between 1 and 100, when you click on it.
# b) Make the button "Click me!" display a number between 1 and 100 in the shiny app, when you click it.
# c) Make the number in the console and number in the app the same random number between 1 and 100.
#optional: Make a new button that removes the random number from the app.
#optional(hard): Make the "Remove"-button diasppear, when there is no number.


library(shiny)
library(shinydashboard)
library(ggplot2)


ui <- dashboardPage(
  dashboardHeader(
    title = "Exercise 2"
  ),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName ="Dashboard_tab", icon = icon("tachometer-alt"))
    )
  ),
  
  dashboardBody(
    tabItems(
      tabItem(tabName = "Dashboard_tab",
              actionButton("actionButtonClickMe", "Click Me!", icon = NULL, width = "200px"),
              textOutput("outputText"),
              actionButton("removeButton", "Clear", icon = NULL, width = "200px")
              )
    )
  )#body
  
)#ui end


server <- function(input, output) {
  
  number <- reactiveValues()
  
  observeEvent(input$actionButtonClickMe, {
    output$outputText <- renderText({
      #print(runif(1,1,100))
      number$random <- runif(1,1,100)
      print(number$random)
    })
    })
  
  observeEvent(input$removeButton, {
    output$outputText <- renderText({
      print("")
    })
  })
}#server end

 
shinyApp(ui, server) #Run app


########## HINTS ###########
# a) Look up 'ObserveEvent()'

# b) Look up 'RenderText()'

# c) Loop up 'reactiveValues()'

# optional: You can have an 'Output$...' that is empty 

# optional(hard): Look up 'renderUI()' (We'll talk more about this later)