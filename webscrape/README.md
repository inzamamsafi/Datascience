This webscrape folder contains 4 files:
1. Flipkart_webscraper.ipynb
2. Dataset
3. Prediction_code.ipynb
4. Readme

# **1. Flipkart_webscraper.ipynb**
In this code I made a webscraper for flipkart to extract the data from flipkart website.
I exctracted the laptop data such as laptop name, ram, hdd, os, screen size, and price.
However the code may not function in future because when websites got updated thier Html format like class name got changed.

So all you need to do is change the class name only and it will hardly takes 2 minutes. 
and after that the you should run the code and you will get the final file in csv format containg all the details.

# **2. Dataset**

After running the _Flipkart_webscraper.ipynb_ you will get the dataset in csv format.

# **3. Predition_code.ipynb**

This is the code thorugh which you will be able to predict the price of laptop using the specifiaction.
In this code i did 3 work
  **A.** Data cleaning
  **B.** Encoding
    Becuase all the features where catorical and without encoding it is not possible to train our data.
  **C.** Standarising, Spliting and training the data.
  
 # Final notes
  
  I got the accuracy of 99%. This can furthure imporve with hypertuning and feature engineering.

