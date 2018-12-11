---
layout: post
title: Transform Excel into a translation tool using this VBA macro  
lang: english
categ: article
keywords: visual basic, vba macros, macro, translation tool, translation tool in excel
tags: [management]
---

## A brief preface
This summer I did an internship at [_BSH Hausgeräte_](https://en.wikipedia.org/wiki/BSH_Hausger%C3%A4te) (aka _Bosch and Siemens Home Appliances_), where I built a lot of amazing tools on _Excel_ using _VBA (Visual Basic for Applications)_. I helped them automate monthly reports, which now take just a few seconds to complete. I would've contribute a lot more to the company if not for the corporate restrictions, according to which I wasn't authorized to access code from other departments.

Anyway, while I signed _NDA_ for the tools I've built for them, I developed tools to help my other routine, which included translating texts sent from our Istanbul headquarter to all subsidiaries in CIS and North Africa. I will share one of them below.

## Translation tool

If you frequently translate texts, you know that a lot of phrases within a domain are repeated, and you probably have your own shortcuts to deal with them. I used _MS Office_'s standard _Find and Replace_ tool to translate the most frequent repetitions.

My VBA macro automates this process as follows: you create an Excel document with original phrase in the first column and its translation in the corresponding cell in the second one, and save it. No column names, no anything else. This file will work as your translation database --- you can always add a new phrase as a new row. 

<figure class="blog">
	<img src="/assets/img/bsh/translate.png">
	<figcaption>Example translation database</figcaption>
</figure>

Then you run the script below in any _MS Word_ file with the original text, and it goes over every phrase in the first column of your Excel database, finds it in the Word file and replaces it with its translation from the second column.

If you know a little Visual Basic, you will understand the code below:

```visualbasic
Sub translation_tool()

Dim objExcel As New Excel.Application
Dim exWb As Excel.Workbook
Dim exSh As Worksheet
        
   
Set exWb = objExcel.Workbooks.Open("path_to_translation_database.xlsx")
Set exSh = exWb.Sheets("Sheet1")
  

For I = 1 To 100
	Selection.Find.ClearFormatting
	Selection.Find.Replacement.ClearFormatting
	With Selection.Find
		.Text = exSh.Cells(I, 1).Value
		.Replacement.Text = exSh.Cells(I, 2).Value
		.Forward = True
		.Wrap = wdFindContinue
		.Format = False
		.MatchCase = False
		.MatchWholeWord = False
		.MatchWildcards = False
		.MatchSoundsLike = False
		.MatchAllWordForms = False
	End With
	Selection.Find.Execute Replace:=wdReplaceAll
	Next I
 

exWb.Close 
End Sub

```

This translation database grows exponentially as you translate more text in your domain. With time it becomes so large that you will just press the button and will only need to slightly edit the resulting translated text.

**Important** there is one caveat though: you must add longer phrases before the shorter ones, because otherwise it will translate individual words first and won't be able to recognize the phrase itself.

Here you go, enjoy. For collaboration [press here](/#hire).
