import requests
from bs4 import BeautifulSoup

def get_stop_name(stop_id: int) -> str:
    # Get page and create soup
    r = requests.get("https://transitfeeds.com/p/adelaide-metro/1/latest/stops?q=" + str(stop_id))
    soup = BeautifulSoup(r.content, "html.parser")
	
	# Find the table that contains the link, find the link that contains the name
    table = soup.find("table", class_="table table-striped table-hover")
    a_tag = table.find("a")
    
    # Get the name and return it
    stop_name = a_tag.decode_contents()
    return stop_name

def main() -> None:
	maryvale = get_stop_name(17346)
	print(maryvale)
	
	return

if __name__ == "__main__":
	main()
