def insert_text_after(file_content, previous_text, text):
    if file_content.find(previous_text) < 0:
        return file_content
    insert_point = file_content.find(previous_text) + len(previous_text)
    new_file_content = file_content[:insert_point]
    new_file_content += text
    new_file_content += file_content[insert_point:]

    return new_file_content
