def validate_questions(data):

    if len(data["questions"]) != 3:
        return False

    return True

    for question in data["questions"]:

        if len(question["options"]) != 4:
            return False
        
        if question["correct_answer"] not in ["A", "B", "C", "D"]:
            return False

        if not question["question"].strip():
            return False

        if not question["explanation"].strip():
            return False