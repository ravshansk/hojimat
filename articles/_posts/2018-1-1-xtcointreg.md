---
layout: post
title: Introducing Panel FMOLS/DOLS command for Stata
lang: english
categ: article
keywords: stata, cointreg, pedroni, panel data
tags: economics
redirect_from: /blog/2018/01/01/xtcointreg/
---
Last week I was hired to perform a thorough analysis of a panel dataset for export dynamics of different sectors in a country. I had never done panel econometrics before or even read it in a textbook. But since I am good at cross-section and time-series, I believed I could handle the task. And I wasn't wrong.  

Since this task was single time with no generalizations/automations required, my tool of choice was of course Stata. It doesn't have a scalability like R but has a very comfortable syntax. You ask me what about E-views? E-views sucks.  

However, in process I realized that panel FMOLS cannot be done natively in stata. The closest thing is `xtpedroni` but it gives panel DOLS and didn't add panel FMOLS. R also doesn't have such a library. Ironically, E-views turned out to have that feature. But I wouldn't concede that easy. So, I decided to go back to [Pedroni's 1996 paper](https://econpapers.repec.org/article/tprrestat/v_3a83_3ay_3a2001_3ai_3a4_3ap_3a727-731.htm) and examine the structure of panel FMOLS estimators. It turned out to be a simple average between each panel's FMOLS for coefficients and sum divided by the square root of the total number of panels for t-statistics.  

So, I got that and tried to write a code for it, but it turned out to be very challenging. Then I found out that there is actually an existing tool for time series FMOLS estimation called `cointreg`. This is an excellent program written by [Qunyong Wang and Na Wu](http://ageconsearch.umn.edu/bitstream/229441/2/sjart_st0272.pdf). So, I just applied the group mean averaging to it.

Meet a new command for Stata `xtcointreg`. It basically adapts `cointreg` to a panel environment, so you need to [install it first](http://agec    onsearch.umn.edu/bitstream/229441/2/sjart_st0272.pdf). The documentation is the same as `cointreg` plus one option `full`. I will submit the file to "ssc". In the meantime you can [download the .ado file here](/assets/ftp/xtcointreg.ado) and place it in the folder called "ado" located inside your system directory(which can be found with a command `sysdir'). 

Hope it will help you in your research. Please feel free to [contact me](/contact) with any questions and commments. 

**Update** It was included to SSC. You can use `ssc install xtcointreg` to download it.  

**Update 2** If you have installed the program successfully but it is not working for some reason, please try this workaround:  
1. write a command `which xtcointreg` and find the location of the **xtcointreg.ado** file;
2. open that file with any text editor and remove the line number 8 `capt program drop xtcointreg`;
3. save the file and try to run `xtcointreg` again. This problem is related to the publisher of the code and not to my code itself.
