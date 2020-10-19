import re


def parse_text(text):
    out = []
    regex = r"<\@(.*)\|.*?>\s(.*)"
    matches = re.finditer(regex, text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            out.append(match.group(groupNum))            
    return out