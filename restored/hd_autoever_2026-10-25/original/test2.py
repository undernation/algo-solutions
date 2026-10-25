# 작성한 코드를 채점하려면 이 파일을 실행하세요
import skeleton2

tc_tickets = [
    ["ai", "mobility", "tech", "ml"],
    ["bronze", "silver", "gold", "platinum"],
    ["c", "cpp", "java", "python", "rust"],
    ["low", "medium", "high"],
    ["tier1", "tier2", "tier3", "tier4", "tier5"]
]

tc_requests = [
    [
        ["09:00", "09:30", "tech", "ai"],
        ["09:30", "10:00", "mobility", "ai"],
        ["17:00", "17:30", "ml", "mobility"]
    ],
    [
        ["10:00", "11:00", "gold", "bronze"],
        ["10:30", "11:30", "platinum", "gold"],
        ["12:00", "13:00", "silver", "bronze"]
    ],
    [
        ["15:00", "16:00", "rust", "python"],
        ["08:00", "09:00", "java", "c"],
        ["09:00", "10:00", "cpp", "c"],
        ["11:00", "12:00", "python", "java"]
    ],
    [
        ["10:00", "11:00", "high", "medium"],
        ["12:00", "13:00", "medium", "high"]
    ],
    [
        ["09:00", "10:00", "tier2", "tier1"],
        ["10:00", "11:00", "tier3", "tier2"],
        ["11:00", "12:00", "tier4", "tier3"],
        ["12:00", "13:00", "tier5", "tier2"]
    ]
]

# 각 테스트케이스별 기댓값(정답)
anslist = ["ml", "gold", "rust", "low", "tier5"]

score = 0
for i in range(len(tc_tickets)):
    res = skeleton2.solution(tc_tickets[i], tc_requests[i])
    if res == anslist[i]:
        score += 20

print("점수 : ", score)