# Public company-history dataset

The CSV files in this directory are small factual extractions from public Infosys investor reports. They were created independently for this repository; they are not exports from a commercial data service. The machine-readable release record is in [`PROVENANCE.yml`](PROVENANCE.yml).

## Sources

| `source_id` | Rows supported | Public source |
| --- | --- | --- |
| `infosys_ar_2012` | FY2007–FY2012 revenue, profit and employees | [Infosys Annual Report 2011–12, Additional Information](https://www.infosys.com/content/dam/infosys-web/en/investors/reports-filings/annual-report/annual/documents/ar-2012/PDFs/Additional_Information_12.pdf) |
| `infosys_ar_2021` | FY2012–FY2013 operating profit and margin; cross-checks for later years | [Infosys Annual Report 2020–21, Historical Data](https://www.infosys.com/investors/reports-filings/documents/additional-information-2020-21.pdf) |
| `infosys_ar_2026` | FY2014–FY2026 financials and employees | [Infosys Annual Report 2025–26, Historical Data](https://www.infosys.com/investors/reports-filings/documents/additional-information-2025-26.pdf) |
| `infosys_ar_2010_segmentation` | FY2010 geographic revenue percentages | [Infosys FY2010 Revenue Segmentation](https://www.infosys.com/content/dam/infosys-web/en/investors/reports-filings/annual-report/annual/documents/ar-2010/Additional-Information/Revenue-Segmentation.html) |
| `infosys_ar_2026_consolidated` | FY2026 business-segment revenue | [Infosys FY2026 Consolidated Statements](https://www.infosys.com/investors/reports-filings/annual-report/annual/documents/2025-26/consolidated.pdf) |
| `infosys_investor_faq` | FY2014–FY2026 dividend per share | [Infosys Investor FAQ](https://www.infosys.com/investors/shareholder-services/faqs.html) |
| `infosys_ar_2024` | FY2024 free cash flow | [Infosys Integrated Report FY2024](https://www.infosys.com/investors/reports-filings/annual-report/annual-reports/ar-2023-24.html) |
| `infosys_ar_2025` | FY2025 free cash flow | [Infosys Integrated Report FY2025](https://www.infosys.com/investors/reports-filings/annual-report/annual-reports/ar-2024-25.html) |

The [Infosys annual-report index](https://www.infosys.com/investors/reports-filings/annual-report/annual-reports.html) is the stable starting point for the complete filings.

## Interpretation notes

- Financial values are in ₹ crore; employee figures are fiscal year-end headcount.
- `net_profit_inr_crore` follows the profit/PAT historical series presented by Infosys. Later filings also present profit attributable to owners, which can differ slightly.
- The long series crosses changes in accounting standards and presentation. It is suitable for broad trend analysis, not a claim that every year is definitionally identical.
- Blank operating fields for FY2007–FY2011 are intentional. We did not fill them from the restricted archive or splice in a differently defined series.
- Geographic percentages compare two issuer-presented snapshots. They are not a claim that every intervening classification was unchanged.
- Business-mix labels are shortened for chart readability; the source filing contains the full segment definitions.
- Dividend figures are adjusted by the issuer for bonus shares and stock splits and include special dividends where reported.
- Revenue per employee in the public report is an author calculation: revenue in crore × 10,000,000 ÷ fiscal year-end employees. It is a directional productivity proxy, not billings per average employee.

The CSV contains reported facts and an original selection/arrangement. The repository’s MIT licence applies to code, not to third-party source documents or marks. Consult the linked reports for context and authoritative wording.
