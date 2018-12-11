---
layout: post
title: Using matching with quotas to solve Hajj visa problem
lang: english
categ: article
description: This matching mechanism solves the problem of unfair visa allocation to Saudi Arabia during Hajj season. 
keywords:  economic consultant, hire economist
tags: economics management
image: /assets/img/kojima/hajj.jpg
---

### Contents
<ul class="index">
<li><a href="#intro">1. Introduction</a></li>
<li><a href="#problem">2. The problem</a></li>
<li><a href="#solution">3. Solution</a></li>
</ul>


<a name="intro"></a><br>
## 1. Introduction

Hajj is the annual event in Mecca, Saudi Arabia, where 1-2 million pilgrims are hosted. This creates an enormous logistic challenge both to the kingdom of Saudi Arabia and to all countries with Muslim population. The former have to host people and determine the annual capacity of the city of Mecca, and the latter have to allocate people in their countries to assigned lots/quotas.

The Foreign Policy journal [discusses the visa allocation in detail](http://foreignpolicy.com/2015/09/23/how-to-score-a-ticket-to-the-hottest-event-in-saudi-the-hajj/). The rule of thumb, Saudi Kingdom uses today, is to give 1000 visa quotas for every 1 million Muslim Population.

<a name="problem"></a><br>
## 2. The problem

The importance of Hajj (_promised complete indulgence from all the previous sins_) makes the trip very desirable to a lot of people. This creates a huge supply-demand misallocation.

The basic economic method (_increasing visa fees until supply meets demand_) is forbidden by religion, as it would create unfairness in the society and leave out non-rich people.

Moreover, the visa allocation within countries is completely left to their respective governments. This creates different methods of visa allocation on site, like bribing officials (until supply meets demand), doing weighted lotteries, creating special commissions deciding who _"deserves"_ to go to Hajj.

The problem with this two-step procedure is (i) inefficiency, due to strict quotas and (ii) no mechanism to punish local bribes.

The inefficiencies include:

- Wasted unfilled quotas [in some countries](https://realnoevremya.com/articles/696)
- Difficulty to determine the actual size of Muslim population (especially in secular states)
- Failure to differentiate between federal and unitary governments (e.g. two separate quotas for Tatarstan and Dagestan, both parts of Russian Federation with citizens holding identical passports making it imposible to differentiate them.)


<a name="solution"></a><br>
## 3. Solution

I propose to use method, proposed by Kamada and Kojima’s in their 2015 [paper on “Efficient matching under distributional constraints”](https://econpapers.repec.org/article/aeaaecrev/v_3a105_3ay_3a2015_3ai_3a1_3ap_3a67-99.htm), to solve this problem. They used the algorithm to improve UK's two-step medical student admission procedure.  

The first step is to revoke the authority of the local governments in visa allocation, since they are either inefficient, corrupt or don’t care (e.g. secular countries). 

Next we use a _Flexible Deferred Acceptance Mechanism (FDA)_ to allocate visas directly to the global population. This will require a new _“Meccan preference set”_ which will favor first-timers and older pilgrims, will not separate family members (a lot of preference criteria can be included in this step).

In order to mimic Kojima’s paper we introduce _“Umrah”_ variable. Umrah is the same ritual as Hajj but which happens any other time throughout the year except for the Hajj season.

Umrah alse has a quota problem, though not that big. So, we introduce 11 variables for 11 months of Umrah to mimic the different "hospitals" to which pilgrims are applying to. The potential pilgrims will give their preference lists of month at which they want to go to Mecca. So, we will obtain “12
hospitals(months)” with “doctor allocation” with regional caps. As a reminder, below is the FDA
mechanism from Kojima’s paper:

<figure class="blog">
	<img src="/assets/img/kojima/fda.png"/>
	<figcaption>Flexible Deferred Acceptance Mechanism by Kamada and Kojima (2015)</figcaption>
</figure>

