# Raw Data Documentation

This directory contains the original, immutable raw financial dataset used for the project.

## File: `Financial_Sample.xlsx`
* **Source:** Microsoft Power BI Financial Sample Tutorial Dataset
* **Official Microsoft URL:** `https://go.microsoft.com/fwlink/?LinkID=521962`
* **Record Count:** 700 transactions
* **Columns (16):**
  1. `Segment`: Commercial customer segment (Government, Midmarket, Enterprise, Small Business, Channel Partners)
  2. `Country`: Geographic market (Canada, France, Germany, Mexico, United States of America)
  3. `Product`: Commercial product line (Carretera, Montana, Paseo, Velo, VTT, Amarilla)
  4. `Discount Band`: Promotional discount tier (None, Low, Medium, High)
  5. `Units Sold`: Number of product units delivered
  6. `Manufacturing Price`: Fixed production cost per product unit ($)
  7. `Sale Price`: List price per product unit ($)
  8. `Gross Sales`: Units Sold × Sale Price ($)
  9. `Discounts`: Total promotional discount deducted ($)
  10. ` Sales`: Net recognized revenue after discount deduction ($) *(note leading whitespace in raw header)*
  11. `COGS`: Cost of Goods Sold ($)
  12. `Profit`: Net Sales - COGS ($) *(accounting definition: Gross Profit)*
  13. `Date`: Transaction date (2013-09-01 to 2014-12-01)
  14. `Month Number`: Integer month (1 - 12)
  15. `Month Name`: Calendar month string
  16. `Year`: Calendar year (2013, 2014)

> **Integrity Note:** This raw file is preserved in its untouched original state. All cleaning, formatting, and star schema transformations are performed downstream by `python/data_cleaning.py`.
