
# columbia-dsi-faculty-scraper

A small web-scraping project built to extract faculty information from Columbia University’s Data Science Institute–related faculty listings.

## Background / Motivation

At the time of writing this project, I was preparing applications for Data Science Master’s programs and, like many others, considered Columbia University. I wanted to tailor my application by referencing faculty whose research aligned with my interests.

That turned out to be harder than expected.

The faculty directory was presented as a single, dynamically loaded page with dozens of profiles rendered at once. There was no easy way to filter, sort, or search by research area, department, or keywords. Scrolling through it manually was noisy, slow, and frustrating.

Instead of forcing myself through it, I did what felt more natural at the time: I scraped the page.

## Approach

The initial attempt used a headless browser, which failed due to dynamic content loading and client-side rendering. The page relied heavily on JavaScript, so static requests were insufficient.

The solution was to:

* Use Selenium to control a real browser instance
* Let the page fully render and load all faculty entries
* Extract structured information such as:

  * Name
  * Department / school
  * Title
  * Profile metadata
* Write the extracted data directly to a text file
* Run basic keyword searches over the output to identify potentially relevant faculty

The search logic was simple and crude, but it was enough to get usable signal without manually combing through the page.

## Files

* `columbia_faculty.py`
  Main Selenium-based scraper script.

* `columbia_faculty.ipynb`
  Notebook version used for experimentation and inspection.

* `README.md`
  This file.

## Notes

* This project predates my use of LLMs or modern tooling for text search or semantic matching.
* The scraping logic is intentionally straightforward and not production-hardened.
* Keyword matching was basic and not particularly effective, but it solved the immediate problem.

## Why I did this?

This project exists because scraping and building a workaround was genuinely more enjoyable than the application process itself.

It reflects a recurring pattern: when faced with an unstructured, tedious task, I tend to reach for code first—not because it’s optimal, but because it’s engaging. This scraper is less about the output and more about the instinct to turn friction into something programmable.

If anyone finds it useful, that’s a bonus.