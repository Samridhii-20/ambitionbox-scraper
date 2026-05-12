import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime


BASE_URL = (
    "https://www.ambitionbox.com/"
    "list-of-companies?page={}"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# =====================================
# SESSION
# =====================================

session = requests.Session()

session.headers.update(HEADERS)


# =====================================
# CLEAN HTML TEXT
# =====================================

def clean_text(html_text):

    if not html_text:
        return "N/A"

    soup = BeautifulSoup(
        html_text,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )


# =====================================
# GET COMPANY LINKS
# =====================================

def get_company_links():

    company_links = []

    visited = set()

    for page in range(1, 6):

        print(
            f"\n[PAGE] Scraping page {page}"
        )

        url = BASE_URL.format(page)

        try:

            response = session.get(
                url,
                timeout=20
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            company_cards = soup.find_all(
                "div",
                class_="companyCardWrapper"
            )

            print(
                f"Companies found: "
                f"{len(company_cards)}"
            )

            # 10 companies per page
            for card in company_cards[:10]:

                try:

                    name_tag = card.find(
                        "h2",
                        class_="companyCardWrapper__companyName"
                    )

                    url_tag = card.find(
                        "meta",
                        itemprop="url"
                    )

                    if (
                        name_tag
                        and url_tag
                    ):

                        company_name = (
                            name_tag.text.strip()
                        )

                        company_url = (
                            url_tag["content"]
                        )

                        if (
                            company_url
                            not in visited
                        ):

                            visited.add(
                                company_url
                            )

                            company_links.append({

                                "Company Name":
                                company_name,

                                "Profile URL":
                                company_url,

                                "Page":
                                page
                            })

                            print(
                                f"[SUCCESS] "
                                f"{company_name}"
                            )

                except Exception as e:

                    print(
                        "[CARD ERROR]",
                        e
                    )

            time.sleep(
                random.uniform(2, 5)
            )

        except Exception as e:

            print(
                "[PAGE ERROR]",
                e
            )

    return company_links


# =====================================
# SCRAPE COMPANY DETAILS
# =====================================

def scrape_company_details(company):

    print(
        f"\n[SCRAPING] "
        f"{company['Company Name']}"
    )

    try:

        response = session.get(
            company["Profile URL"],
            timeout=20
        )

        if response.status_code != 200:

            print(
                "[BLOCKED]",
                company["Company Name"]
            )

            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # JSON DATA
        script_tag = soup.find(
            "script",
            id="__NEXT_DATA__"
        )

        if not script_tag:

            print(
                "[FAILED] No JSON found"
            )

            return None

        json_data = json.loads(
            script_tag.string
        )

        page_props = (
            json_data["props"]
            ["pageProps"]
        )

        company_meta = (
            page_props
            ["companyMetaInformation"]
        )

        ratings_section = (
            page_props
            ["aggregatedRatingsData"]
            ["ratingDistribution"]
            ["data"]
        )

        ratings = (
            ratings_section
            .get("ratings", {})
        )

        # Industries
        industries = []

        primary = company_meta.get(
            "primaryIndustry",
            []
        )

        secondary = company_meta.get(
            "secondaryIndustry",
            []
        )

        for item in primary:

            industries.append(
                item.get("name")
            )

        for item in secondary:

            industries.append(
                item.get("name")
            )

        result = {

            "Company Name":
            company_meta.get(
                "shortName",
                "N/A"
            ),

            "Profile URL":
            company["Profile URL"],

            "Overall Rating":
            company_meta.get(
                "rating",
                "N/A"
            ),

            "Total Reviews":
            ratings_section.get(
                "totalCount",
                "N/A"
            ),

            "Industry":
            ", ".join(industries),

            "Company Summary":
            clean_text(
                company_meta.get(
                    "description"
                )
            ),

            "Salary Rating":
            ratings.get(
                "compensationBenefitsRating",
                "N/A"
            ),

            "Job Security Rating":
            ratings.get(
                "jobSecurityRating",
                "N/A"
            ),

            "Work-Life Balance Rating":
            ratings.get(
                "workLifeRating",
                "N/A"
            ),

            "Scraped At":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        print(
            f"[DONE] "
            f"{result['Company Name']}"
        )

        time.sleep(
            random.uniform(2, 5)
        )

        return result

    except Exception as e:

        print(
            "[DETAIL ERROR]",
            e
        )

        return None


# =====================================
# SAVE FILES
# =====================================

def save_files(data):

    if not data:

        print("No data found.")
        return

    df = pd.DataFrame(data)

    # CSV
    df.to_csv(
        "companies.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # JSON
    df.to_json(
        "companies.json",
        orient="records",
        indent=4
    )

    print(
        "\nFiles saved successfully!"
    )


# =====================================
# MAIN
# =====================================

def main():

    print(
        "\n========== STARTING SCRAPER ==========\n"
    )

    company_links = get_company_links()

    print(
        f"\nCollected "
        f"{len(company_links)} companies"
    )

    all_data = []

    for company in company_links:

        details = scrape_company_details(
            company
        )

        if details:

            all_data.append(
                details
            )

    save_files(all_data)

    print(
        "\n========== SCRAPING COMPLETED =========="
    )

    print(
        f"Total companies scraped: "
        f"{len(all_data)}"
    )


if __name__ == "__main__":

    main()