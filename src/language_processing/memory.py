from datetime import datetime
import json

# Save raw_ json on memory/exp/...json
# Save resume_ on memory/day-resumes/...txt
def save_day_resume(raw_json, resume_):
    current_date = datetime.now().strftime("%Y-%m-%d")
    with open(f'./memory/exp/{current_date}.json', 'w') as file:
        json.dump(raw_json, file, indent=4)
    with open(f'./memory/day-resumes/{current_date}.txt', 'w') as file_resume:
        file_resume.write(resume_)