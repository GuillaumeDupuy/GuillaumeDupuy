import os
import requests

blc = ">-"

url = "https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key="+os.environ['WAKATIME_API_KEY']
DEL_START  ="<!--WAKATIME-->"
DEL_END    ="<!--/WAKATIME-->"
n = 0
mustachefile=open('main.mustache','r')
lines = mustachefile.readlines()
mustachefile.close()

start =-1
end = -1
for line in lines:
    if DEL_START in line:
        start = n
    if DEL_END in line:
        end = n
    n+=1
if start == -1 or end == -1:
    print("Error: Delimiter not found")
    exit(1)
partONe = lines[:start+1]
conttemp = lines[start+1:end]
partTwo = lines[end:]
r = requests.get(url)

r = r.json()

def col(pers):
    result = ""
    for i in range(10):
        t = pers - i*10
        if t <= 0:
            result += blc[1]
        else:
            result += blc[0]
    return result + " " + str(pers) + " %"


txt = ["```text\n","⌚ Total time: "+r["data"]["human_readable_total_including_other_language"]+"\n","\n"]

temp = []
maxName = 0
maxText = 0

txt.append("💬 Languages:\n")
txt.append("\n")

for i in r['data']['languages']:
    if len(i["name"]) > maxName:
        maxName = len(i["name"])
    if len(i["text"]) > maxText:
        maxText = len(i["text"])
    temp.append([i['name'],i['percent'],i['text']])

for i in temp:
    txt.append(i[0]+(" "*(maxName-len(i[0])+1))+ i[2]+(" "*(maxText -len(i[2])+1)) +col(i[1])+"\n")


txt.append("\n")
txt.append("🔥 IDE:\n")
txt.append("\n")

temp = []
maxName = 0
maxText = 0

for i in r['data']['editors']:
    if len(i["name"]) > maxName:
        maxName = len(i["name"])
    if len(i["text"]) > maxText:
        maxText = len(i["text"])
    temp.append([i['name'],i['percent'],i['text']])

for i in temp:
    txt.append(i[0]+(" "*(maxName-len(i[0])+1))+ i[2]+(" "*(maxText -len(i[2])+1)) +col(i[1])+"\n")

txt.append("\n")
txt.append("💻 OS:\n")
txt.append("\n")

temp = []
maxName = 0
maxText = 0

for i in r['data']['operating_systems']:
    if len(i["name"]) > maxName:
        maxName = len(i["name"])
    if len(i["text"]) > maxText:
        maxText = len(i["text"])
    temp.append([i['name'],i['percent'],i['text']])

for i in temp:
    txt.append(i[0]+(" "*(maxName-len(i[0])+1))+ i[2]+(" "*(maxText -len(i[2])+1)) +col(i[1])+"\n")

txt.append("```\n")


if conttemp == txt:
    print("No change in main.mustache")
    exit(0)
result = partONe + txt + partTwo
mustachefile=open('main.mustache','w')
mustachefile.writelines(result)
mustachefile.close()
os.system('git config --local user.email "github-actions[bot]@users.noreply.github.com"')
os.system('git config --local user.name "github-actions[bot]"')
os.system('git add .')
os.system('git commit -m "wakatime update"')
os.system('git push')