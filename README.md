# enable_lead_generation
Compile a list of restaurants in Qatar for B2B lead generation

<strong> Objective </strong>
In this task, we will build a one-time automation tool that helps compile a comprehensive list of restaurants in Qatar that offers delivery and are potential clients to be approached by Enable. The ultimate goal is to produce a list of restaurants that are filtered by the number of branches, and fine dining category. The list shall be handed over to the business team, which should apply its own methods to identify businesses to approach.  


<strong> Data Sources </strong>

Talabat: List of nearly all companies in Qatar that offer delivery service 
Google Maps: The Google Maps API will help us count the number of branches of each restaurant.  
MyBookQatar: The mobile app indicates the number of branches each brand has.  
Snoonu: It contains a category called fine dining which we can use to filter the “big” list.  
Open Table: We can use the estimated price range to filter fine dining.  


<strong> Example </strong>

Talabat = 3,317 are non-food vendors such as flower shops, and pharmacies  
Google Maps = 120restaurants has only 1 branch 
MyBookQatar = 50 restaurants has only 1 branch 
Snoonu = 300 restaurants are fine dining 
Open Table = 100 restaurants are fine dining 

Total number of restaurants: 3,317 - 120 - 50 - 300 - 100 = 2,747 
