---
layout: post
title: Valuation Calculator for Subscription-Based Businesses
lang: english
categ: article
description: R reimplementation of Daniel McCarthy and Peter Fader's valuation model
keywords: peter fader, R, economics, management, stock, valuation, IPO, public data, subscription
tags: economics management finance
redirect_from: /blog/2018/09/09/subvalue/
image: /assets/img/churn/diag2.png
---

Last summer I worked on a project that used Daniel McCarthy, Peter Fader and Bruce Hardie's valuation model, described in their paper "Valuing Subscription-Based Businesses Using Publicly Disclosed Customer Data" available at [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2701093#maincontent).

Their model features a lot of series, vectors, matrices, intertwined recursive definitions, that it was very difficult to comprehend at first. So, if you are going to read their paper, here is the diagram that I have drawn to make it easier for you to understand it. 

<figure class="blog">
	<img src="/assets/img/churn/diag.png" height="300%">
	<figcaption>McCarthy et al.'s Customer behavior model</figcaption>
</figure>

In the summer gig, I mentioned, I had to use an Excel-based optimization kindly provided by Dan Mccarthy, due to time constraints. But now I finally found time to replicate their model in R.

It's in an earliest alpha version now, and does not optimize consistently. Moreover, I haven't built a Shiny user interface due to my workload on other projects.

However, if you are interested, you can find the code in the [Github repo that I created specifically for that](https://github.com/ravshansk/danmccarthy). You are welcome to contribute to the project. I will welcome your pull requests.

Ideally, the project will constitute an open-source user-friendly valuation calculator for subscription-based businesses.

Let's combine our codes to make life easier for laymen!
