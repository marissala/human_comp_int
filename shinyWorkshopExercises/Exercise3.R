#############################################################################
#################### Assigment 3 - Outputs from inputs ######################
#############################################################################
# a) Create a textInput and an actionButton in the UI.
# Task 1: When you open the app and write something in the textInput and press the button,
#         the text that you have written must appear below button as verbatimText.
#
# Task 2: Until the user has submitted any text, the verbatimText must say "No 
#         text has been submitted yet".
#
# Task 3(hard): As soon as the user has written just one letter in the textInput,
#               some additional elements (such as sliderInput or selectInput), must
#               appear in the app. 

library(shiny)
library(shinydashboard)
library(ggplot2)
pacman::p_load(shinyjs)


ui <- dashboardPage(
  dashboardHeader(
    title = "Exercise 3"
  ),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName ="Dashboard_tab", icon = icon("tachometer-alt"))
    )
  ),
  
  dashboardBody(
    tabItems(
      tabItem(tabName = "Dashboard_tab",
              textInput("writeInText", "Write here"),
              actionButton("EnterText", "Enter"),
              verbatimTextOutput("value"),
              # shinyjs::hidden(
              #   sliderInput("sliding", "Choose your fav number",
              #             min = 0, max = 1000, value = 500),
              #   plotOutput("distPlot")
              # ),
              uiOutput("interactiveUI")
      )
    )
  )#body
)#ui end


server <- function(input, output) {
  texted <- reactiveValues()
  texted$presence <- FALSE
  
  observeEvent(input$EnterText, {
    texted$text_input <- input$writeInText
    texted$presence <- TRUE
    shinyjs::show("sliding")
    show("distPlot")
  })
  
  output$value <- renderText({
    if (texted$presence) {
      texted$text_input
    } else {
      print("No text has been submitted yet")
    }
  
  })
  
  output$interactiveUI <- renderUI({
    if(nchar(input$writeInText)>0)
    tagList(sliderInput("sliding", "Choose your fav number",
                        min = 0, max = 1000, value = 500)#,
            #plotOutput("distPlot", hist(rnorm(input$sliding)))
            )
  })
  
  # output$distPlot <- renderPlot({
  #   if (texted$presence) {
  #     hist(rnorm(input$sliding))
  #   } else {
  #     print("Choose a value on the slider!")
  #   }
    
  #})
}#server end


shinyApp(ui, server) #Run app