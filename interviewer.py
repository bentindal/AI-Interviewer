from openai import OpenAI
import datetime

client = OpenAI()

interview_position = input('What role are you applying for? \n>> ')
interview_name = input('What is your name? \n>> ')
interview_prompt = f'I want you to act as an interviewer. I will be the candidate and you will ask me the interview questions for the {interview_position} position.  My first sentence is "Hi"'

message_list=[
    {"role": "system", "content": interview_prompt},
    {"role": "user", "content": f"I want you to only reply as the interviewer. Do not write all the conservation at once. I want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write explanations. Ask me the questions one by one like an interviewer does and wait for my answers. After asking 3 questions I want you to let me know whether I got the job or not and how well I scored. You have to tell me whether I got the job or not straight away after the interview. Make sure to tell me my score at the end of the interview out of 10. After the interview write '=== INTERVIEW OVER ==='. My name is {interview_name}. Ask me my first question about {interview_position}."}
  ]
interview_in_progress = True

while interview_in_progress:
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=message_list
    )

    msg = response.choices[0].message.content
    message_list.append({"role": "user", "content": msg})

    words = msg.split()
    for word in words:
        if word == '===' or word == 'INTERVIEW' or word == 'OVER' or word == '===':
            interview_in_progress = False
            break
    if interview_in_progress:
        print(f'\n{msg}')
        input_msg = input(">> ")
        message_list.append({"role": "system", "content": input_msg})

print(f'\n{msg}')

# Save the conversation to a text file
time_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dir_location = f'{time_now}_{interview_name}_interview_report.txt'
message_list = message_list[2:]

with open(dir_location, 'w') as f:
    for item in message_list:
        f.write("%s\n" % item['content'])

print(f'\nInterview Report saved to {dir_location}')