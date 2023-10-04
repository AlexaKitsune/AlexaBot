ADJUST_RANGE = 15
ADJUST_STEPS = 1
LIMIT_DEGREE = 30

steps_eyes_x = 0
steps_eyes_y = 0

def eyes(vision_data):
    if vision_data is not None:
        global steps_eyes_x
        global steps_eyes_y
        global ADJUST_STEPS

        if steps_eyes_x > LIMIT_DEGREE:
            steps_eyes_x = LIMIT_DEGREE
            ADJUST_STEPS = 2
        elif steps_eyes_x < -LIMIT_DEGREE:
            steps_eyes_x = -LIMIT_DEGREE
            ADJUST_STEPS = 2

        if steps_eyes_y > LIMIT_DEGREE:
            steps_eyes_y = LIMIT_DEGREE
            ADJUST_STEPS = 3
        elif steps_eyes_y < -LIMIT_DEGREE:
            steps_eyes_y = -LIMIT_DEGREE
            ADJUST_STEPS = 3

        detected_object = vision_data["bigger_object"]
        detected_object = {
            "name": detected_object["objectType"],
            "center_x": detected_object["center"][0]-320,
            "center_y": detected_object["center"][1]-240
        }

        difference_x = int(detected_object["center_x"])
        difference_y = int(detected_object["center_y"])

        if -125 < difference_x < -95 or 95 < difference_x < 125:
            ADJUST_STEPS = 2
        elif difference_x > 125 or difference_x < -125:
            ADJUST_STEPS = 3

        if -125 < difference_y < -95 or 95 < difference_y < 100:
            ADJUST_STEPS = 2
        elif difference_y > 125 or difference_y < -125:
            ADJUST_STEPS = 3


        if -ADJUST_RANGE <= difference_x <= ADJUST_RANGE:
            steps_eyes_x = steps_eyes_x
            ADJUST_STEPS = 1
        else:
            if(difference_x < 0):
                steps_eyes_x += ADJUST_STEPS
            else:
                steps_eyes_x -= ADJUST_STEPS

        if -ADJUST_RANGE <= difference_y <= ADJUST_RANGE:
            steps_eyes_y = steps_eyes_y
            ADJUST_STEPS = 1
        else:
            if(difference_y < 0):
                steps_eyes_y += ADJUST_STEPS
            else:
                steps_eyes_y -= ADJUST_STEPS

        result = {
            "difference_x": steps_eyes_x * -1 ,
            "difference_y": steps_eyes_y
        }

        if(difference_y < ADJUST_RANGE and -10 <= difference_x <= 10):
            ADJUST_STEPS = 1
            steps_eyes_y += 1

        #print(result, ADJUST_STEPS, [difference_x, difference_y])
        print(steps_eyes_y)
        return result


def jaw(text_):
    print(">>> ", text_)
    text_ = text_.lower()
    result = []
    final_result = []

    for letter in text_:
        if letter in " ":
            result.append("L")
        elif letter in "bcdfghjklmnñpqrstvwxyz":
            result.append("M")
        elif letter in "aeiouáéíóú":
            result.append("H")
        else:
            pass

    text_ = "".join(result).split("L")
    
    for word in text_:
        if(len(word) > 4):
            final_result.append("H")
        else:
            final_result.append("M")
    
    final_result = {
        "tts_tokens": "M".join(final_result)
    }
    
    print(final_result)
    return final_result