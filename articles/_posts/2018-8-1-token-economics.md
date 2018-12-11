---
layout: post
title: Utility tokens&#58; discussion, economic model and simulation in R
lang: english
categ: article
description: economic model of utility tokens in R
keywords: cryptocurrency, token, ethereum, proof-of-stake, hackernoon, economics, token economics, tokenomics
tags: crypto economics
redirect_from: /blog/2018/08/01/tokens/
image: /assets/img/token/tokenomy.png
---

[_This post has been originally published in HackerNoon. Click here to read the original._](https://hackernoon.com/utility-tokens-discussion-economic-model-and-simulation-in-r-798c0ff3d26c)  

Last fall I was hired to build an economic model for _token-curated registries_ as part of my [consulting job](/#hire). Since then, I encountered many people who expressed interest in this model, so I decided to share the basic theory and implementation. 

### Contents
<ul class="index">
<li><a href="#intro">1. Philosophical introduction</a></li>
<li><a href="#model">2. Model summary</a></li>
<li><a href="#agents">3. Agents and motivations</a></li>
<li><a href="#statics">4. System statics</a></li>
<li><a href="#dynamics">5. System dynamics: simulation in R</a></li>
<li><a href="#conclusion">6. Conclusion</a></li>
</ul>

<a name="intro"></a><br>
## 1. Philosophical introduction

**<a href="#model">To skip to the model click here</a>**

The great expositive summary of _Token economy_ can be found on [Wikipedia](https://en.wikipedia.org/wiki/Token_economy), so I will dive into my points straight away.  

As I see it, a token economy is an attempt to quantify life and give a price to everything. This aligns perfectly with classical economic thinking, where even externalities, such as air pollution, can be compensated by sufficient taxes.  

Wikipedia says that tokens have been successfully used at schools and psychiatric hospitals, but the recent resurgence in interest has begun with the cryptocurrency rush. Since the creation of universally accepted token was problematic before, nobody tried to tie all services to some price. However, the open source blockchain algorithms made this process really easy and suddenly many people decided that it is a good idea to _tokenize_ (read _monetize_) literally everything.  

Being an economist myself, I believe that this thinking is terribly wrong. I understand where it comes from --- everybody took  _Econ 101_ at some point and was inspired by elegance of _invisible hand_ models. But I also know that _free market_ is not the only mechanism out there. _Centralized matching mechanisms_, _social planner's problem_, _lotteries_ all exist for a reason. Not every _equilibrium_ is _efficient_. Sadly, not everybody takes advanced econ courses, while almost everybody wants to profit from _ICO_'s.  

<div class="highlighted">Not every equilibrium is efficient</div>

Of course, tokens can be justified in appropriate cases. Actually, the great working area for tokens is online games, where every crystal is given a price and has an obvious value to players. In general, whenever any kind of labor is involved, a money making procedure is good. Otherwise, it is some kind of _rent seeking_.  

Ryan Selkis of _Messari_ [greatly summarized](https://medium.com/tbis-weekly-bits/skin-in-the-game-coins-da0afdfdc650) the difference between _bubble_ and _utility tokens_, and explained why he believes the former will be worthless in the long run. I will go even further and claim that most so-called utility tokens are as well bubbles and don't give any extra utility.  

### **Examples**

Below I reviewed a couple of examples that appear in the first results page when you google _utility tokens_. 

[Datum](https://datum.org/assets/Datum-WhitePaper.pdf) claims to help users to prevent social networks from collecting their data "for free" and sell it for money instead, _i.e._ _"take control"_ of their information. This certainly sounds fun, but it totally neglects the fact that Facebook or Youtube are already providing a great service for free in exchange for collecting users' data, moreover they offer all kinds of privacy settings for all their users. It is a fair trade. What Datum wants is to take those services for granted and try to profit from that, providing no utility whatsoever.

[Talenthon](https://www.talenthon.io/docs/whitepaper_talenthon.pdf) wants to make another LinkedIn but to replace reputational structure with token structure and give tokens for truthful references. That's wrong on many levels, including:

- impossibility to quantify references
- possibility that worker can change, making references obsolete
- the assumption that businessmen would care about tokens more than they care about their reputation

This is exactly what I meant above, when I said that monetary relationships are not always efficient. And finally, these people hypocritically encourage openness and decentralization while using proprietary algorithms.  

<div class="highlighted">The right decision is to only decentralize those services that actually support the decentralization.</div>

Another issue with _token-backed decentralization_ is that historically every decentralization was tightly related to _disruption, hippie philosophy, anarchy_. All examples of successful decentralization used to be altruistic and didn't involve monetary goals. Decentralized apps (DAPPs) I care for are _BitTorrent, Wikipedia, Linux, GNU Project, OpenStreetMap_ etc.  

Decentralized projects used to be the very definitions of _trust-based systems_, where corporations like _Apple_ would be put to shame by the community for not contributing code back to _BSD_ but still get away with it, and nobody would attempt to financially incentivize them to do so.  

<div class="highlighted">These old days, which most of us still remember, should raise everyone's concerns about the longevity of trustless structures.</div>

There are, however, appropriate use cases for tokens and some developers get this.  

[AdChain](https://adtoken.com/uploads/white-paper.pdf) does this well by aiming at a peculiar area --- ranking ads services. This is compatible with token system and is not something that has already been done on a massive scale.  

[Filecoin](https://filecoin.io/filecoin.pdf) does even better job by providing a service of renting storage space, which works at the same time as a mining tool via _proof-of-storage_. They have problems with modelling incentives but at the end of the day they provide legit utility and thus are _not bubbles_.   

In this article I will try to build an economic model for exactly those _utility tokens_. 

<a name="model"></a><br>
## 2. Model summary 

This economic model of tokens is very generic, so that it can work as a blueprint for future token creators and as a reasonable abstraction for applied economists.

<div class="highlighted">Ideally, this model can also serve as a guideline for writing whitepapers.</div> 

In case you have skipped the previous section, let me remind you that _utility tokens_ are any tokens that produce a legit service for consumers and are not _primarily_ tools for middlemen or speculators (although such agents do exist in our model).  

Since tokens aim at _trustless_ structures, we will need some kind of proof that every _node_ corresponds to a single person instead of some _botnet_. Since I am a huge [_proof-of-work_](https://en.wikipedia.org/wiki/Proof-of-work_system) opposer and since most of the tokens are built on Ethereum platform, which is [moving towards _proof-of-stake_](https://cointelegraph.com/news/first-version-of-ethereums-casper-update-has-been-released) anyway, I will use the latter in the model.  

<div class="highlighted">The service is paid for in fixed number of tokens, not in cash.</div>

Pricing service in a fixed token rate will correctly capture the proportionate relationship between demand and price --- the greater the demand for the service, the more people will buy tokens, the price of tokens will increase, and so will the cash equivalent of the service; and vice versa.  

There are consumers, investors, and honest and malicious miners in our model, each having different _motivations_ and _types_. Consumers and malicious miners want token price to depreciate, while honest miners and investors want token price to appreciate.  

The incentives should be modelled in such a way that no player will want to deviate from the honest sutainable system as long as there is an honest majority (_conditional equilibrium_). We will assume the [_Ethereum Casper_](https://arxiv.org/abs/1710.09437)'s _checkpoint tree_ voting model, as it satisfies the _accountable safety_ and _plausible liveness_ as long as _2/3_ of votes are honest. We will model the resulting economy but not dig into the technicalities or revisit what _Vitalik Buterin_ and _Virgil Griffith_ have already spent some time to model. 

<a name="agents"></a><br>
## 3. Agents and motivations

In a general _utility token economy_ there are four types of agents:

### Honest miners
Honest miners are people with domain expertise, who actually do the job and create the utility. They are incentivized by a system to do the best job they can to earn more tokens as long as they constitute _51%_ of the _active_ token holders.  

They do not play any _strategies_, _i.e._ they naively vote for the correct version in every quorum. They earn (mine) rewards as long as malicious miners don't take over, and at the same time they provide a utility to customers. Therefore the main quantitative feature of honest miners is their proportion among all miners. 

<div class="highlighted">Main quantitative feature of honest miners is their number.</div>

The corresponding issue is that it is impossible to tell for certain which miners are honest and which are not. Therefore customers and investors choose their strategies based on the expectations. The prior probabilities which form these expectations are exogeneous in this model but can be endogenized. If you are a researcher interested in extending the model in this area, please [contact me](/#contact), so that we can discuss and share the ideas on that topic.


### Customers
Customers are people who use and benefit from the service created by the _honest miners_ and pay for it using tokens they bought for cash. 

As mentioned in the introduction, utility tokens only work good in peculiar services like job referencing or ads ranking. Therefore, customers not only care about the quality of service, but also about its popularity/public acceptance. This can be modelled using the following version of _Cobb-Douglas utility function_:

<figure class="blog">
	<img src="/assets/img/token/cust_util.png" width="50%" alt="Customer's utility function">
	<figcaption>Customer's utility function</figcaption>
</figure>

where _E[x]_ is the expected demand and _E[z]_ is the expected number of experts (honest miners) in the system.  

Note that even when there is zero demand but nonzero number of experts (_E[x]=0; E[z]>0_) the customer still receives a non-zero utility from the service. Conversely, when the service is very popular and has high demand but zero expert knowledge (_E[x]>0; E[z]=0_) the utility from the service is zero despite its popularity.

<div class="highlighted">The demand for tokens is equal to the expected total number of customers</div>

The customers are not uniform though --- there are _early adopters_, _late majority_ and _laggards_. They differ in reservation utility levels --- each type of customer will only subscribe to the service if the utility _U(x,z)_ will exceed _U<sub>early</sub>, U<sub>late</sub>, U<sub>lag</sub>_ respectively, where _U<sub>early</sub> &le; U<sub>late</sub> &le; U<sub>lag</sub>_.  

According to [_product adoption life cycle_](https://en.wikipedia.org/wiki/Technology_adoption_life_cycle), the consumer types are distributed as _16%_ early adopters, _68%_ late majority and _16%_ laggards:

<figure class="blog">
	<img src="/assets/img/token/cust_dist.png" width="60%" alt="Customer type allocation">
	<figcaption>Modified Roger's curve</figcaption>
</figure>

You can see that I have simplified the actual Roger's curve. If you are interested in extending the model to use actual technology adoption lifecycle, you can [contact me](/#contact) and I will share my ideas.

### Investors
Investors are people who buy tokens for _ICO_/market value and hold them in expectation of value appreciation. We will assume that there are _N_ identical investors with equal wealth level _w_, who are using a version of _Markowitz's mean-variance formula_ to choose between investing in stocks and our tokens.  

<figure class="blog">
	<img src="/assets/img/token/markowitz.png" width="30%" alt="Markowitz formula">
	<figcaption>Modified Markowitz's mean-variance formula</figcaption>
</figure>

where _&mu;<sub>c</sub>_ and _&mu;<sub>s</sub>_ are coin and stock returns respectively, and _&gamma;_ and _&sigma;<sub>c</sub>_ are risk-aversion coefficient and coin volatility.  

Note that we simplify and consider stock returns _deterministic_, so the model can be extended here. You can also replace Markowitz with more complex and more realistic models like _Merton_, _Munk_, _Bodie_, _Samuelson_ or _Campbell_ or add other cryptocoins into the decision. Since our model aims to be as generic as possible, we leave out these options. If you are interested in financial economics and want to extend the model in this area, please [contact me](/#contact) so that we can share ideas and/or collaborate.

We will also assume that all the investors are risk neutral.  

For further simplicity, we will omit _gamblers_ from our model --- the investors who will strategically predict the quorum outcome and vote in that direction to mine extra tokens. Those, who are interested in that, can enhance on this model themselves and/or [contact me](/#contact) for ideas and suggestions.    

<div class="highlighted">The more investors a system has, the more cash is in the system.</div>


### Malicious miners
Malicious miners are people who buy tokens for _ICO_/market value and vote at quorum to force their version of blockchain.  

In this model we don't consider hypothetical _Jokers_ (_i.e._ system trolls who want to sabotage the honest blockchain just for the sake of it), so all malicious miners have a rational agenda --- it's almost always the profit maximization outside of the system.  

<figure class="blog">
	<img src="/assets/img/token/malprofit.png" width="90%" alt="Malicious miner's profit">
	<figcaption>Malicious miner's profit</figcaption>
</figure>

where the first term is the initial profit a company makes by selling their good or service at price _f_ to their initial consumers plus a share of total demand that comes from the token vote with probability  _&alpha;_ of winning the vote. The second term is the _interference term_ which completes probability of demand from tokens to _1_ at the cost of buying tokens necessary to win the majority vote at price _p<sub>c</sub>_ per token. The second term is equal to zero in case of non-interference, _i.e._ no malicious token activity.   

<div class="highlighted">The more malicious miners a system has, the easier it is for them to influence the votes.</div>

Malicious miners participate in the token economy only if spending cash on tokens and winning the votes will increase their outside profit. Otherwise, they won't have any incentive to meddle with the blockchain.  

In this model we assume that all malicious miners want to lobby the single version o the blockchain and not conflict among themselves. Moreover, malicious miners can preemptively buy tokens while they are cheap to increase profits in the future, even if this decision does not increase short-term profits. If you are interested in extending the model in this area, please feel free to [contact me](/#contact) to discuss this and exchange ideas.





In the next section we will quickly see how these agents interact at a fixed point in time.

<a name="statics"></a><br>
## 4. System statics

At any point in time, the agents solve their corresponding utility maximization problems from the previous section. The generalized static interactions can be visualized as follows:

<figure class="blog">
	<img src="/assets/img/token/tokenomy.png" width="70%" alt="Token economy system statics">
	<figcaption>System statics in a utility token economy</figcaption>
</figure>

Note that we differentiate between _active_ and _passive_ tokens, where former participate in votes and the latter do not. 

To model the price formation of a token we use a simplified version of _quantity theory of money_ with money market equilibrium modelled in [_"Economics of Bitcoin Price Formation"_](https://arxiv.org/pdf/1405.4498.pdf) (Ciaian et al. (2014)).

<figure class="blog">
	<img src="/assets/img/token/price.png" width="30%" alt="Price of token formula">
	<figcaption>Price formula of token</figcaption>
</figure>

where _PY_ is the dollar value of a token economy, _r_ is the opportunity interest rate (in our case, _&mu;<sub>s</sub>_), _T_ is the size of token supply and  _&eta;_ is an exogeneous stabilization parameter.  

Note that in a proof-of-stake economy, the token supply _T_ is fixed, so the token is _deflationary_.  

To calculate the nominal GDP (_PY_) we add all the cash that customers and investors inject in the token economy.


If you are interested in more complicated pricing formulas, please read Ciaian's paper, mentioned above, and/or [contact me](/#contact) to exchange ideas.  
<a name="dynamics"></a><br>
## 4. System dynamics: simulation in R
Previous two sections summarize the economy at any fixed point in time. To see how this system works over time we need to perform a dynamic analysis. The system dynamics can be modelled to follow the timing described below:  
1. The economy begins when developers create the protocol and generate all the tokens (see Section 2). _Without loss of generality_, we assume that there is only one creator. 

2. Creator distributes a certain share of all tokens to early experts who agree to work for tokens instead of cash and not sell them for at least a certain period of time. We make a weak assumption that all these early experts are _honest_ miners. She sells other tokens in an _ICO_.  

    The decision how much to keep, how much to sell and how much to distribute involves a whole optimization process on its own, but we exogenize it for simplicity. As always, any [extensions are welcome](/#contact).

3. Consumers decide whether to subscribe to the service by buying tokens or to opt for other service providers.  

    Investors decide whether to buy tokens or stocks instead.  

    Malicious miners decide whether buying tokens and joining the vote will increase their short-term profit. 

4. All market participants are determined and active tokens are bidden in a vote. 
  
5. Majority vote wins, and losers' stakes are _slashed_ --- equally redistributed among winners.

6. Consumers' and investors' cash injections are calculated and added to price formula. Token's price is updated.

    Current token rate of return is calculated as _(1 + &Delta;p<sub>t</sub>/p<sub>t</sub>)_

    Token's attractiveness parameter _&eta;_ is updated. 

    Current stock rates of returns _r_ are observed.

7. Loop steps 3 to 6.


### R simulation

We are ready to see how the economy will work in a simulation. First we will define the default parameters. 
```R
# PERIODS
N <- 100      #number of time periods of interest

# AGENTS
n_D <- 1000   #maximum potential subscription demand
n_I <- 200    #number of investors
n_H <- 100    #number of honest miners
n_M <- 30     #number of malicious miners
n_HB <- 50    #number of honest beneficiaries

# MARKET PARAMETERS
mu_s <- 0.2   #stock rate of return (assume deterministic)
f <- 100      #unit price of malicious miner's side product
n_T <- 100000 #total number of tokens
distsh <- 0.5 #share distributed to experts
fee <- 5      #service fee in tokens

# UTILITY PARAMETERS
eta <- 1      #token's attractiveness
alpha <- 1    #Cobb-Douglas weight of popularity
beta <- 1     #Cobb-Douglas weight of expertise
U_early <- 0  #reservation utility for early adopters
U_late<-16000 #reservation utility for late majority
U_lag <-84000 #reservation utility for laggards

# customer distribution
n_Dearly <- 0.16*n_D #number of early adopters
n_Dlate <- 0.68*n_D  #number of late majority
n_Dlag <- 0.16*n_D   #number of laggards

n_B <- included * n_M + n_HB    #expected total beneficiaries
```

Then we initialize the main results matrix:

```R
results <- data.frame(token_price=rep(1, N),
                      num_customers=n_Dearly,
                      cash_invested=0,
                      stock_rate=mu_s,
                      num_honest=n_H
                      )
```

Assuming that 160 early adopters each bought 5 tokens in the first period for exchange rate _1 token = 1 $_ and each of 200 investors also bought 10 tokens, we have the size of the token economy in the first period equal to 2800. Plugging that into price equation gives the real token value of _0.14_, but we use this information in an unusual way and assign it as an appreciation in the first period:

```R
results$cash_invested[1] <- 2000
results$token_price[2] <- 1.21 
```

What I just did, doesn't really make any sense --- I just had to arrive at a workable Markowitz solution somehow. So, if anyone wants to propose a good price appreciation mechanism, [please contact me](/#contact) and I will correct that. 

And finally, we run a simulation for _N_ periods. 

```R
# run the simulation
for(t in 2:N){
  # CUSTOMERS
  #calculate utility
  U = (1 + results$num_customers[t-1])^alpha * results$num_honest[t-1]^beta
  #decide whether to enter or not
  if(U>=U_lag){
    results$num_customers[t] <- n_Dearly + n_Dlate + n_Dlag
  }else if(U<U_lag & U>=U_late){
    results$num_customers[t] <- n_Dearly + n_Dlate
  }else if (U<U_late & U>=U_lag){
    results$num_customers[t] <- n_Dearly
  }
  
  # INVESTORS
  #calculate rate of return:
  token_rate <- results$token_price[t]/results$token_price[t-1] - 1
  #calculate sharpe ratio
  sharpe_ratio <- (token_rate - mu_s)/(5*0.01)
  #invest in the token
  results$cash_invested[t] <- n_I * 100 * sharpe_ratio
  
  
  # MALICIOUS MINERS
  prior_profit <- included * f * results$num_customers[t] / (n_B) 
  enter_profit <- 1 * f * results$num_customers[t] /  (n_HB + n_M) - results$token_price[t] * (0.51 - included) * (n_H + n_M) / n_M
  
  
  # TOKEN PRICE
  results$token_price[t+1] = eta * (results$num_customers[t] * fee + results$cash_invested[t]) / (mu_s * n_T)
}

```

This basic implementation gives _rudimentary_ results, like price and demand dynamics etc.

<figure class="blog">
	<img src="/assets/img/token/numcustomers.png" width="50%" alt="Demand dynamics">
	<img src="/assets/img/token/tokenprice.png" width="50%" alt="Token price">
	<figcaption>Token price and demand dynamics</figcaption>
</figure>


<a name="conclusion"></a><br>
## 6. Conclusion

In this article I have discussed my opinion on the current state of crypto-tokens and built a universal economic model of utility tokens. Since this model is very generic, **_the realistic results can only be obtained by tailoring it to your specific use case_**. However, this framework and the corresponding R script are the great start to model any utility token economy.  

Whether you are a researcher or token developer, I believe this framework will be useful to you in analyzing token economies. I welcome every discussion on model extensions and/or improvements.  

I strongly believe that open knowledge is the only way to the progress. You are free to use any of the components of the article, but **_I kindly ask you to cite the source_** and let other people read this article and contribute to the discussion. The publishable version of this paper is not ready yet, but I can send you a draft version [on demand](/#contact).  

I kindly want to remind that economic consulting [is my job](/#hire), so I can provide any help with tailoring the model to your needs, but this will be a [paid service](/#hire). You can hire me via [email](mailto:rsk@ravshansk.com) or by [filling the Hire Me form](/#hire). Please be sure to include the estimated budget, the scope and the deadlines.

