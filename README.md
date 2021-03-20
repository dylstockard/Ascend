# Ascend
Dawgs:
  Dylan Stockard
  Ece Oz

Challenge Statement: Develop an automated solution for the restuarant American Son (owned by Chef Tim Ma) that will read, categorize, and summarize reviews into a report.

Solution: We created a program that can scrape OpenTable, an online reservation and review website for restaurants such as Chef Tim's American Son, to read in the reviews left by users. We then analyzed reviews as positive or negative, and categorized these reviews into 5 categories:
  - Brunch: reviews concerning American Son's brunch menu.
  - Dinner: reviews concerning American Son's dinner menu.
  - Food: reviews concerning the general quality and taste of the food.
  - Ambience: reviews concerning the mood and feel of the restaurant setting.
  - Service: reviews concerning the quality of service provided by the restaurant.
After categorizing the reviews, we calculated valuable statistics and auto-generated a PDF that visualized the customer reviews so that Chef Tim can know at a glance what his customers and did and didn't enjoy with their meal at American Son.
We also listed reviews that were deemed useful based on character length and category in the PDF so that if Chef Tim wanted to read the reviews anyway, he could read reviews concerning exactly what category he was interested in, and avoid reviews that provide no constructive criticism.

Currently, we run the program to produce the PDF report on our end, and then upload it to a google drive that Chef Tim can access after being notified that a new PDF is created. This way he has no responsibilities of his own to create the report, and just has to retrieve from google drive.

Moving forward, we would expand this program to generate review reports for any small business, and this can be done just by changing the URL that we scrape our reviews from American Son's webpage to someone elses. We can also move our PDF to a web application format so that users can get updates whenever they want, and in an interactive format. The potential for growth is unlimited.
