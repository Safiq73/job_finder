import re

def findExperienceOccurrence(text):
    # Yrs
    pattern = re.compile(r'\b(?:years|yrs)\b', re.IGNORECASE)
    matches = re.finditer(pattern, text)
    occurrences = [text[max(match.start()-10,0): min(len(text), match.end())] for match in matches]
    return occurrences

def isExperienceEligible(occurrences: list, users_exp: int):
    # {"-", "t", "+", "y"}
    for occurrence in occurrences:
        
        occurrence = occurrence.replace(" ", "")
        for chr in occurrence:
            if chr.isnumeric():
                if int(chr)> users_exp:
                    return False
                break
    return True

