---
layout: post
title: My take on the famous medical appointment no-show problem  
lang: english
categ: article
description: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
keywords: machine learning, economic consulting, economic consultant, statistical consulting, statistical consultant, data science, data scientist
tags: [statistics, economics]
image: /assets/img/munkfin/nobel.jpg
---


### Contents
<ul class="index">
<li><a href="#intro">1. Introduction</a></li>
<li><a href="#data">2. Data exploration</a></li>
<li><a href="#class">3. Classifier</a></li>
<li><a href="#class">4. Conclusion</a></li>
</ul>


<a name="intro"></a><br>
## 1. Introduction

This is a [famous problem from Kaggle website](https://www.kaggle.com/joniarroba/noshowappointments). We have a dataset of online medical appointments in the city of Vitória, Espírito Santo in Brazil. It turns out that in a period of three months between May and August, 2016, patients did not show up in 25% of appointments. To investigate the possible reasons behind this, we will analyze the data and make inferences.

<a name="data"></a><br>
## 2. Data exploration


### Outliers
First of all, we explore the dataset. We immediately notice that some age values are negative, and very old patients don't exhibit variation having too few observations:

<figure class="blog">
	<img src="/assets/img/brazil/tableage.png">
	<figcaption>Frequency table of age data points</figcaption>
</figure>

Moreover, some appointments have been done to the dates before it was scheduled, probably, due to some system error. We remove the obvious outliers from our data, combine all data points for households older than 80 (to balance subset size), and continue with our analysis.

```r
df <- df[ (df$age >= 0) & (df$dayap >= df$daysc),]
```

### Demographic factors

#### Age factor
Observing the no-show dynamics throughout lifetime, gives important insights to our analysis:

<figure class="blog">
	<img src="/assets/img/brazil/agenoshow.png">
	<figcaption>Percentage of patients who showed up, by age</figcaption>
</figure>

From common experience, we know that appointments for patients younger than 18, are actually done by their parents. We can see how, as kids grow older, the parents tend to miss more appointments (because new parents tend to be concerned more with infant's health, and as kids grow, parents tend to neglect their health slightly more).

As kids grow into young adults, they start steadily taking their health seriously and miss less appointments.

Also, for patients older than 80, we don't have many data points at particular ages, so we aggregated them into one group.

So, we use two possible age variables: a continuous one with two dummies for 18 and 80 year olds, and a discrete variable correpsonding to 11 decades of patients.

#### Gender factor
Another demographic factor is gender. The probability distribution shows that gender does not play a significant role in no-show rate:

<figure class="blog">
	<img src="/assets/img/brazil/sexnoshow.png">
	<figcaption>Show-up probability, by gender</figcaption>
</figure>

We tried to look at adults only (age>=18), because usually mothers (female=1) go to doctors with their children, irrespective of the kid's registered gender, but this procedure returned no significant difference either:

<figure class="blog">
	<img src="/assets/img/brazil/sexnoshow18.png">
	<figcaption>Show-up probability for grown-ups only, by gender</figcaption>
</figure>

Thus, we ignore gender in further discussion.

### Geographic factor
Looking at no-show rates by neighbourhood shows relative balance, with only a few outliers, which do not round to 20\%.

```r
rayonXnoshow <- table(df$rayon, df$noshow)
plot(unique(df$rayon),rayonXnoshow[,2]/(rayonXnoshow[,1]+rayonXnoshow[,2]),type = "n", ylab="probability of showing up", xlab="Vitoria neighbourhoods")
rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "#e5e5e5")
grid(col="white", lwd=2)
lines(unique(df$rayon), rayonXnoshow[,2]/(rayonXnoshow[,1]+rayonXnoshow[,2]), type="h", lwd=5, col="#f8766d")
```

We see that most (not all) of the outliers come from neighbourhoods with little data:

```r
plot(df$rayon,type = "n", ylab="number of data points", xlab="Vitoria neighbourhoods")
```

Therefore, we ignore neighbourhoods with less than 40 data points to avoid wrong statistics (e.g. in Parque Industrial there is only one registered appointment and it shows 100% show-up rate, which is incomparable with neighbourhoods with thousands of observations.) So, we ignore neigbourhoods _Aeroporto, Ilha do Boi, Ilha do Frade, Ilhas Oceanicas de Trinade, and Parque Industrial_.

Now, we still have outliers (we considered 3% to be a significant deviation from the average, 20%) in percentage of no-shows, which have sufficient observations not to ignore them. They are: _Solon Borges, Santos Dumont, Santa Clara, Santa Cecilia, Itarare, De Lourdes, Do Cabral, Do Quadro, Horto, Jardim Da Penha, Jesus de Nazareth, Mario Cypreste, and Santa Martha_. 

We will add dummy variables for these 13 neighbourhoods as our geographic predictors. Other neighborhoods will be assumed to contribute no new information to the expected value.

```r
df$solbor <- ifelse(df$rayon=="SOLON BORGES",1,0)
df$sandum <- ifelse(df$rayon=="SANTOS DUMONT",1,0)
df$sancla <- ifelse(df$rayon=="SANTA CLARA",1,0)
df$sancec <- ifelse(df$rayon=="SANTA CECÍLIA",1,0)
df$itarar <- ifelse(df$rayon=="ITARARÉ",1,0)
df$lourde <- ifelse(df$rayon=="DE LOURDES",1,0)
df$cabral <- ifelse(df$rayon=="DO CABRAL",1,0)
df$quadro <- ifelse(df$rayon=="DO QUADRO",1,0)
df$horto  <- ifelse(df$rayon=="HORTO",1,0)
df$penha  <- ifelse(df$rayon=="JARDIM DA PENHA",1,0)
df$jesus  <- ifelse(df$rayon=="JESUS DE NAZARETH",1,0)
df$cypres <- ifelse(df$rayon=="MÁRIO CYPRESTE",1,0)
df$sanmar <- ifelse(df$rayon=="SANTA MARTHA",1,0)
```

### Temporal factor
Temporal data brings the crucial information about the appointment no-shows, starting from the weekday of the appointment, and ending with the wait time. Since we don't have at least a year-long data, we cannot speak of seasonality patterns, and will have to get by with what we have.


#### Weekdays
The day of the week is the first thing that comes to mind - during the weekdays, patients might have emergencies at school or at work, and this could cause them to miss the appointment. However, the analysis shows no significant difference through week, except for Saturdays:

```r
plot(table(df$wdaysc, df$noshow)[,2],type='n',ylim=c(0,0.25), xlab="days of week", ylab="probability of no-show")
rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "#e5e5e5")
grid(col="white", lwd=2)
lines(prop.table(table(df$wdayap,df$noshow),1)[,2], type="o", col="blue", lwd=5)
lines(prop.table(table(df$wdaysc,df$noshow),1)[,2], type="o", col="#f8766d", lwd=5)
legend(x="bottomleft", legend = c("weekday of schedule", "weekday of appointment"), fill = c("blue", "#f8766d") )
```

But further analysis shows that this happens because of the lack of enough data for Saturday:

```r
table(df$wdayap,df$noshow)
table(df$wdaysc,df$noshow)
```

So, we ignore the weekdays and assume that they don't affect the no-show rate.

#### Wait time
Another obvious variable is a wait time from scheduling the appointment to the appointment itself. It is plausible to assume that in longer wait times patients can get cured, book another earlier appointment, or die before the appointment.

We define the "days between" variable as the difference between "day of appointment" and "day of schedule":

```r
df$daybw <- as.numeric(df$dayap - df$daysc)
```

The plot below shows that when appointments are scheduled in that same day (wait time = 0), the patient almost never misses it (just 4\% no-show rate). There is sufficient data (34\% of all observations) to support this claim.

```r
daybwXnoshow <- table(df$daybw, df$noshow)
plot(prop.table(daybwXnoshow,1)[,2], type="n", xlab="# wait days", ylab="probability of no-show")
rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "#e5e5e5")
grid(col="white", lwd=2)
lines(prop.table(daybwXnoshow,1)[,2], type="h", col="#f8766d", lwd=3)
```

In the next days, the no-show rate is very volatile. To avoid weekly seasonality, we aggregate the data by weeks. Also, for two reasons: _(i)_ since the longer wait times have small data points and _(ii)_ since (assuming time discounting --- a weak economic assumption) people perceive recent past clearer than distant past, we aggregated first month as 4 weeks, and aggregated the next data points by month:

```r
daybwXnoshow <- table(df$daybw, df$noshow)
waitsex <- rowsum(daybwXnoshow,c(0, rep(1:4,each=7), rep(5:7,each=30), rep(7,10)))
dimnames(waitsex) <- list(c("0 days", "1 week", "2 weeks", "3 weeks", "4 weeks", "2 months", "3 months", "4 months"),c("show", "no show"))
prop.table(waitsex,1)
```

Note that _4 months_ wait is an outlier due to small dataset. Otherwise, all probabilities after 1 week fall into &plusmn;3\% interval. Taking this and _(ii)_ into consideration, suggests an even wilder (yet still plausible) aggregation: _0 days, 1 week, and >1 week_:

```r
daybwXnoshow <- table(df$daybw, df$noshow)
waitsex <- rowsum(daybwXnoshow,c(0, rep(1,7), rep(2,121)))
dimnames(waitsex) <- list(c("0 days", "1 week", ">1 week"),c("show", "no show"))
prop.table(waitsex,1)
```

Thus, we will use three-valued categorical variables to denote wait times.


#### Hour of the day
Lifestyle of people potentially reflects their degree of responsibility --- _"night owls"_ tend to sleep during days and maybe miss deadlines, while _"early birds"_ may take their appointments more seriously. We take a look at the data of time o'clock when the appointment was scheduled. The online appointment system opens at 6AM and closes at 10PM. We divide these 16-hour days into 4 groups of 4, and find that _"early bird effect"_ actually exists, and people who scheduled appointments between 6AM and 10AM are significantly less likely to miss their appointments, while any other time slot does not change the no-show probability significantly:

```r
hourshow <- rowsum(table(df$hoursc, df$noshow), rep(1:4,each=4))
dimnames(hourshow) <- list(c("6AM-10AM:", "10AM-2PM:", "2PM-6PM:", "6PM-10PM:"), c("show", "no show"))
prop.table(hourshow,1)
```

Thus, we use a binary dummy variable --- _6AM-10AM_ or _10AM-10PM_ --- to incorporate time.

### Medical factor

#### Appointment history
To incorporate the idiosyncracies of patients, we use the history of their previous appointments, and whether they missed them before. The table below shows the repeat patients' allocation.

```r
table(df$prev)
```

For every patient, we found the modes (most frequent observations) of previous no-show stats. For patients that appear in the dataset only once, this value will be 0 (performing sensitivity checks we learned that leaving out one-time patients entirely, returns no significant difference (<0.5%) but complicates the dataset, so we chose to set the average previous no-show rate for first-time patients at 0). We observe that such modes greatly contribute to predicting the next no-show:

```r
noprevtable <- table(ifelse(df$noprevpct>=0.5,1,0),df$noshow)
dimnames(noprevtable) <- list(c("mode0:", "mode1:"), c("show", "noshow"))
prop.table(noprevtable,1)
```

#### Patient condition
Patient's medical history can influence the no-show behavior. The tables below show differences in percentage of no-shows for patients with alcoholism, diabetes, hipertension, medical financial assitance (so-called "scholarship"), and handicaps:

```r
burstab <- prop.table(table(df$burs, df$noshow),1)
dimnames(burstab) = list(c("no scholarship", "scholarship"), c("show", "no show"))
burstab
hipertab <- prop.table(table(df$hiper, df$noshow),1)
dimnames(hipertab) = list(c("no hipertension", "hipertension"), c("show", "no show"))
hipertab
diabettab <- prop.table(table(df$diabet, df$noshow),1)
dimnames(diabettab) = list(c("no diabetes", "diabetes"), c("show", "no show"))
diabettab
alcoholtab <- prop.table(table(df$alcohol, df$noshow),1)
dimnames(alcoholtab) = list(c("no alcohol", "alcohol"), c("show", "no show"))
alcoholtab
handcaptab <- prop.table(table(df$handcap, df$noshow),1)
dimnames(handcaptab) = list(c("handicap0:", "handicap1:", "handicap2:", "handicap3:", "handicap4:"), c("show", "no show"))
handcaptab
```

Strangely, alcoholism is the only condition which turned out to not have an effect on no-show probability. The probable reason is that alcoholism is not immediately lethal, and people tend to treat is less seriously than any other _"more serious"_ illness like diabetes. So, we include all of the above conditions, except alcoholism, in our classification.

#### SMS
One can justifiably argue that patients may simply forget their appointment date and time. Hospitals tried to send SMS-reminders to their patients, but does this practice worth the cost? A simple frequency table shows that yes, patients, who received SMS-reminders, were less likely to miss the appointment:

```r
smsnoshow <- prop.table(table(df$sms, df$noshow))
dimnames(smsnoshow) <- list(c("no sms", "sms"), c("show", "no show"))
smsnoshow
```
 
#### Overall no-show stata
Finally, we decided to include the general historical average of noshows till the moment by all patients. However, this complicated the random sampling, and, most importantly, didn't affect the final result much (because it had little variation over time). So, we did not include this variable. 

<a name="class"></a><br>
## 3. CLassifier

We used _logit_ (logistic regression) and _decision trees_ to classify the data.

### Logit
```r
df$waittime <- ifelse(df$daybw==0,0,ifelse(df$daybw<=7,1,2))
df$morning <- ifelse(df$hoursc>=6 & df$hoursc<=10, 1, 0)
df$age18 <- ifelse(df$age>=18,1,0)
df$age80 <- ifelse(df$age>=80,1,0)
df$age_decade <- floor(df$age/10)
trainsize <- round(nrow(df)*0.8)
dftrain <- df[1:trainsize,]
dftest <- df[(trainsize+1):nrow(df),]
```

```r
logit <- glm(formula = 
               noshow ~ age + age18 + age80 +
               burs + diabet + handcap + alcohol +
               solbor + sandum + itarar + lourde + cabral + quadro + penha + jesus + sanmar +
               sms + morning + waittime + mode_previous,
             family = binomial(link="logit"),
             data = dftrain
             )
summary(logit)
```

We found that the wait time, previous no-show history, and geographical location were the most important predictors. Also, alcohol turned out to be statistically significant, while hipertension had to be removed from the final model. Strangely, eligibility to financial assistance increased the likelihood of no-show (but this was discussed in the previous section).

To check the accuracy of the model, we predict the no-show for the test data and use measures called _accuracy_ and _AUR_:

```r
predicted_noshow <- ifelse(predict(logit, dftest,type = "response")>=0.5,1,0)
actual_noshow <- dftest$noshow
mytab <- table(abs(predicted_noshow - actual_noshow))

accuracy <- mytab[1]/(mytab[1] + mytab[2])
accuracy
roc(actual_noshow, predicted_noshow)
```

So, we have 81\% accuracy, but this is not a very desirable result because of data imbalance --- if we just set all "noshows" to zero, we would still get 80% accuracy. The measure _AUR_ confirms this by giving the result 52.9\% --- which is slightly better than saying _"fifty-fify"_.

So, we decide to take a look at decision trees:

### Decision trees
The decision tree returns 79\% accuracy and 50.6\% _AUR_ on average. Different tree specifications give different resulting trees, but the average accuracy doesn't change. Here is just one of the trees. Notice that we used age as decades here, and not as a continuous variable:

```r
dtree <- rpart(formula=noshow ~ age_decade + 
                 burs + diabet + handcap + alcohol + hiper + 
                 solbor + sandum + itarar + lourde + cabral + quadro + penha + jesus + sanmar + 
                 sms + morning + waittime + mode_previous,
               data = df,
               method = "class",
               control = rpart.control(xval = 5, cp=0.0000001, minsplit=100)
               )
rpart.plot(dtree)
```

<a name="end"></a><br>
## 4. Conclusion
We have analyzed the data and tried to do a classification analysis. The results are not perfectly accurate, but they are not worse than a naive "noshow=0" prediction.

As an economist, I believe that having a higher accuracy would be impossible without additional data, like weather that day (was it rainy or not), the traffic situation, the diagnosis, the local news etc.

And here, we conclude.
