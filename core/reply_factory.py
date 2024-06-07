
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id==None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["correct_ans"]=0

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)
    session["current_question_id"]=next_question_id

    if next_question!=None:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id!=None:
        if answer==PYTHON_QUESTION_LIST[current_question_id]["answer"]:
            print(session["correct_ans"])
            session["correct_ans"]=session.get("correct_ans",0)+1
    '''
    Validates and stores the answer for the current question to django session.
    '''
    return True,""


def get_next_question(current_question_id):
    if current_question_id==None:
        current_question_id=-1
    if current_question_id>=len(PYTHON_QUESTION_LIST)-1:
        return None,None
    question=PYTHON_QUESTION_LIST[current_question_id+1]["question_text"]+r"%spl%"+"#val".join(PYTHON_QUESTION_LIST[current_question_id+1]['options'])
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    print(question)

    return question, current_question_id+1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    return "Result: total questions asked {} and correct answer {} ".format(len(PYTHON_QUESTION_LIST),session['correct_ans'])
