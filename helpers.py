from bs4 import BeautifulSoup


def get_elements(soup: BeautifulSoup, tag: str, attribute: str, attribute_value: str):
    """Gets all the elements with given features in format requested"""
    # get all elements from the soup
    elements = soup.findAll(tag, {attribute: attribute_value})

    def return_desired_elements() -> list[str]:
        list_to_return = list()
        if tag == "a":
            list_to_return = [element["href"] for element in elements]
        else:
            # default if the desired_format is not given
            list_to_return = [element.text for element in elements]
        return list_to_return
    return return_desired_elements()
