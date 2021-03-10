from urllib.request import urlopen

def scrape_data():
    url = "http://olympus.realpython.org/profiles/aphrodite"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    print(html)

if __name__ == "__main__":
    scrape_data()