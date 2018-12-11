---
layout: post
title: Factor Analysis and Uniform distributions
lang: english
categ: article
description: Product of which distributions is uniform? What is square root of a uniform distribution? I have found a great approximation - Beta(1.2, 0.5) is very intuitive and almost perfect product decomposition of uniform distribution.
keywords: uniform distribution, beta distribution, decomposition 
tags: statistics
redirect_from: /blog/2018/03/27/factoranalysis/
image: /assets/img/factoranalysis/beta21.png
---

[**To learn about product decomposition of uniform distribution click here or keep on reading**](#unifrand)


This month I worked on a [psychometric project](https://en.wikipedia.org/wiki/Psychometrics). It is interesting that I had never heard about this field before. Psychometrics, is basically statistics applied to psychology, similar to econometrics, biostatitcs etc. What is great about my economic background, though, is the rigorous mathematical and statistical background - it helped me learn the subject and contribute fairly quickly.   

The task was to design an algorithm which randomly generates correlation matrices satisfying given [factor analysis model](https://en.wikipedia.org/wiki/Factor_analysis).  

I finished the great textbook "Modern Factor Analysis" by Harry H. Harman and learned a lot. In a nutshell, Factor analysis is the method used to find latent common factors which underlie the given variables; once found, such factors may be used in the model as regressors, thus reducing the number of variables.  

Psychologists use this to evaluate various test results: 100-question test by 1000 people gives a large panel dataset. However if the test questions could be reduced to their underlying hidden factors like introversion, risk aversion, optimism etc. we could considerably simplify the analysis. After all, the measure of those traits (and not the test questions) is _THE_ purpose of psychology.  

Generating correlation matrices was easy, but generating them uniformly was a big trouble. Indeed, a product of two uniform random variables is not uniform. I have discovered a great combination of free terms for [beta distribution](https://en.wikipedia.org/wiki/Beta_distribution) to deal with this problem:

## Product decomposition of Uniform Random variables <a name="unifrand"></a>

First of all, let's recall the density plot of a _uniform distribution_:

<figure class="blog">
	<img src="/assets/img/factoranalysis/unif.png" alt="Uniform distribution">
	<figcaption>Uniform Distribution</figcaption>
</figure>

Unfortunately, the product of uniform distributions is not uniform and is skewed towards origin. So, I decided to find the square root of a uniform distribution. After long inquiries I found a [great proof](http://www.sci.csueastbay.edu/~esuess/classes/Statistics_6401/Handouts/trans/TransUnif.pdf) that square root of the uniform distribution is Beta(2,1) distribution.

<div class="highlighted">Square of a Beta(2,1) distributed variable is uniformly distributed</div>

<figure class="blog">
	<img src="/assets/img/factoranalysis/beta21.png" alt="Beta(2,1) distribution">
	<figcaption>Beta(2,1) Distribution</figcaption>
</figure>

<figure class="blog">
	<img src="/assets/img/factoranalysis/beta21sq.png" alt="Square of Beta(2,1) distribution">
	<figcaption>Square of Beta(2,1) is Uniform</figcaption>
</figure>

Unfortunately, the product of two distinct _i.i.d._ Beta(2,1)-distributed variables was not uniform. So, the above property wasn't useful for the project. But I was inspired now --- I discovered the beta distribution and wasn't going to let it go --- I googled "the product of beta distributions" and found a great deal of related literature (please look it up if you are interested). 

<div class="highlighted">Uniform distribution can be expressed as Beta(1,1) distribution</div>

I discovered that the product formula for two beta-distributed variables was really complex and I decided that the _rigor could be compensated for intuitiveness in this case_, after all this was statistics and not a real analysis.  

After trying to solve for the free parameters and combining this with trial-and-error, I have finally discovered the answer --- the distribution was _Beta(1.2, 0.5)_! 

<div class="highlighted">Product of two Beta(1.2, 0.5)-distributed variables is approximately uniform</div>

The density plot for Beta(1.2, 0.5) looks as follows:

<figure class="blog">
	<img src="/assets/img/factoranalysis/beta1205.png" alt="Beta(1.2,0.5) distribution">
	<figcaption>Beta(1.2, 0.5) distribution</figcaption>
</figure>

The product of two _i.i.d._ variables from this distribution is approximately uniformly distributed, as can be seen below:

<figure class="blog">
	<img src="/assets/img/factoranalysis/beta1205prod.png" alt="Product of Beta(1.2,0.5) variables">
	<figcaption>Product of two Beta(1.2, 0.5)-distributed variables is approximately uniform</figcaption>
</figure>

## Conclusion

I find this discovery extremely enlightening and useful. Hope you will too. To read about my other projects please see my other blog entries.
