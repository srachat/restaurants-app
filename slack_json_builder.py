def create_type(type_):
	return {"type": type_}


def create_divider():
	return create_type("divider")


def create_element_of_type(element_type, element_key, element_value):
	return {
		"type": element_type,
		element_key: element_value,
	}


def create_text_of_type(text_type, text):
	return create_element_of_type(text_type, "text", text)


def create_markdown(text):
	return create_text_of_type("mrkdwn", text)


def create_section(text):
	return create_text_of_type("section", text)
