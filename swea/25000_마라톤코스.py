"""
SWEA 25000  마라톤 코스
https://swexpertacademy.com/main/talk/solvingClub/problemView.do?solveclubId=AZt8IiBqxEDHBIN6&contestProbId=AZih2RXKu2_HBINp&probBoxId=AZt8IiBqxEHHBIN6&type=PROBLEM

풀이일 : 2026-08-24   결과: 못품
한도   : time 25개 테스트케이스를 합쳐서 C++의 경우 3초 / Java의 경우 3초 / Python의 경우 6초 / memory 힙, 정적 메모리 합쳐서 262144 kbytes 이내, 스택 메모리 1024 kbytes 이내 / time_sec 6
난이도 : D6  |  정답률 74.29%
제약   : 1. 각 테스트 케이스 시작 시 init() 함수가 호출된다.
제약   : 2. 하나의 지점에 연결되는 도로는 최대 5개이다.
제약   : 3. 각 테스트 케이스에서 addRoad() 함수의 호출은 최대 1,000 이다.
제약   : 4. 각 테스트 케이스에서 removeRoad() 함수의 호출은 최대 100 이다.
제약   : 5. 각 테스트 케이스에서 getLength() 함수의 호출은 최대 1,000 이다.

[채점] accepted  1/1  (5.576s)

[문제]
[Fig. 1] 과 같이 도시에 N 개의 지점과 도로가 있다. 지점과 지점은 도로로 연결된다.

도로는 양방향 이동이 가능하고, 도로 길이의 단위는 m 이다.

[[IMG:1]]

N 개의 지점 중에 하나의 지점을 출발/도착지점으로 선택해 마라톤 코스를 만들려고 한다.

마라톤 코스의 길이는 42,195m 이하이고, 서로 겹치지 않는 8개의 도로로 구성된다.

[Fig. 1] 에서 파란색 원 지점을 출발/도착지점으로 선택하면, 그림과 같이 8 개의 도로로 구성된 여러 개의 마라톤 코스 중의 하나를 만들 수 있다.

마라톤 코스는 출발 지점에서 시작해서 반환 지점을 거쳐 도착 지점에서 끝난다.

또한, 거꾸로 도착지점에서 시작해서 반환 지점을 거쳐 출발 지점에서 끝나는 마라톤 코스의 길이도 동일하다.

따라서, 마라톤 코스에서 임의의 반환 지점을 모두 찾을 경우, 빠르게 마라톤 코스의 길이를 알 수 있다.

여기에서 반환 지점은 출발 지점에서 시작해서 4개의 도로를 지난 지점이다.

단, 마라톤 코스는 서로 겹치지 않는 8개의 도로로 구성해야 한다.

이와 더불어, 출발/도착 지점은 마라톤 코스 중간에 지나갈 수 없다.

지점들을 연결하는 도로의 정보가 주어질 때, 임의의 지점에서 출발/도착하는 마라톤 코스의 길이를 계산하는 프로그램을 작성하라.

아래 API 설명을 참조하여 각 함수를 구현하라.

※ 아래 함수 signature는 C/C++에 대한 것으로 다른 언어에 대해서는 제공되는 Main과 User Code를 참고하라.

아래는 User Code 부분에 작성해야 하는 API 의 설명이다.

void init(int N)

각 테스트 케이스의 처음에 호출된다.

도시에는 1 부터 N 까지 N 개의 지점이 있고, 지점들을 연결하는 도로는 없다.

Parameters

N: 도시에 있는 지점의 개수 ( 10 ≤ N ≤ 1,000 )

void addRoad(int K, int mID[], int mSpotA[], int mSpotB[], int mLen[])

K 개의 mSpotA[]지점과 mSpotB[]지점을 연결하는 아이디가 mID[], 길이가 mLen[]인 도로들이 추가된다.

mSpotA[i]지점과 mSpotB[i]지점은 서로 다른 지점이고, 연결하는 도로가 없음이 보장된다. ( 0 ≤ i ≤ K-1 )

추가되는 도로들의 아이디 mID[] 는 모두 서로 다르고, 기존 추가된 도로의 아이디와 서로 다르다.

Parameters

K : 추가되는 도로의 개수 ( 1 ≤ K ≤ 10 )

mID[] : 추가되는 도로의 ID ( 1 ≤ mID[] ≤ 1,000,000,000 )

mSpotA[] : 추가되는 도로의 한 지점 ( 1 ≤ mSpotA[] ≤ N )

mSpotB[] : 추가되는 도로의 다른 지점 ( 1 ≤ mSpotB[] ≤ N )

mLen[] : 추가되는 도로의 길이 ( 4,000 ≤ mLen[] ≤ 7,000 )

void removeRoad(int mID)

mID 도로를 삭제한다.

mID 도로가 없거나 mID 도로가 이미 삭제되었을 수도 있다.

Parameters

mID: 도로의 ID ( 1 ≤ mID ≤ 1,000,000,000 )

int getLength(int mSpot)

mSpot 지점을 출발/도착 지점으로 선택할 때, 42,195m 이하의 길이가 가장 긴 마라톤 코스의 길이를 반환한다.

마라톤 코스는 서로 겹치지 않는 8 개의 도로로 구성된다.

8개의 도로로 마라톤 코스를 만들 수 없거나 길이가 42,195m 이하의 마라톤 코스를 만들 수 없을 경우, -1 을 반환한다.

마라톤 코스 구성 시 mSpot 지점은 출발 지점과 도착 지점을 제외하고 지나가지 않는다.

Parameters

mSpot : 마라톤 코스의 출발/도착 지점 ( 1 ≤ mSpot ≤ N )

Returns

출발/도착 지점이 mSpot 지점일 때, 42,195m 이하의 길이가 가장 긴 마라톤 코스의 길이

마라톤 코스를 만들 수 없을 경우, -1

[예제 1]
입력:
25 100
14
100 12
200 add_road_K: 3
add_road_ID: 92 add_road_spotA: 1 add_road_spotB: 3 add_road_Length: 5421
add_road_ID: 721 add_road_spotA: 1 add_road_spotB: 6 add_road_Length: 4885
add_road_ID: 111 add_road_spotA: 7 add_road_spotB: 1 add_road_Length: 5799
200 add_road_K: 4
add_road_ID: 514 add_road_spotA: 6 add_road_spotB: 11 add_road_Length: 5938
add_road_ID: 104 add_road_spotA: 9 add_road_spotB: 8 add_road_Length: 4671
add_road_ID: 103 add_road_spotA: 3 add_road_spotB: 4 add_road_Length: 4785
add_road_ID: 109 add_road_spotA: 2 add_road_spotB: 4 add_road_Length: 5089
400 start_spotA: 1 return_length: -1
200 add_road_K: 5
add_road_ID: 1101 add_road_spotA: 10 add_road_spotB: 8 add_road_Length: 4528
add_road_ID: 724 add_road_spotA: 7 add_road_spotB: 11 add_road_Length: 5715
add_road_ID: 9724 add_road_spotA: 12 add_road_spotB: 11 add_road_Length: 5689
add_road_ID: 150 add_road_spotA: 9 add_road_spotB: 12 add_road_Length: 5858
add_road_ID: 62 add_road_spotA: 8 add_road_spotB: 4 add_road_Length: 4219
400 start_spotA: 1 return_length: 42157
300 remove_road_ID: 724
400 start_spotA: 1 return_length: 41466
200 add_road_K: 6
add_road_ID: 682 add_road_spotA: 7 add_road_spotB: 12 add_road_Length: 5981
add_road_ID: 931 add_road_spotA: 12 add_road_spotB: 6 add_road_Length: 6195
add_road_ID: 709 add_road_spotA: 10 add_road_spotB: 11 add_road_Length: 5194
add_road_ID: 528 add_road_spotA: 10 add_road_spotB: 9 add_road_Length: 5241
add_road_ID: 267 add_road_spotA: 10 add_road_spotB: 3 add_road_Length: 6288
add_road_ID: 162 add_road_spotA: 2 add_road_spotB: 3 add_road_Length: 4997
200 add_road_K: 5
add_road_ID: 317 add_road_spotA: 1 add_road_spotB: 2 add_road_Length: 5008
add_road_ID: 99 add_road_spotA: 3 add_road_spotB: 5 add_road_Length: 5831
add_road_ID: 333 add_road_spotA: 5 add_road_spotB: 6 add_road_Length: 5094
add_road_ID: 241 add_road_spotA: 9 add_road_spotB: 5 add_road_Length: 5165
add_road_ID: 315 add_road_spotA: 4 add_road_spotB: 5 add_road_Length: 5234
400 start_spotA: 6 return_length: 42184
400 start_spotA: 4 return_length: 42139
300 remove_road_ID: 241
400 start_spotA: 7 return_length: 42035
100
100 30
200 add_road_K: 2
add_road_ID: 379425 add_road_spotA: 12 add_road_spotB: 13 add_road_Length: 5344
add_road_ID: 255006 add_road_spotA: 24 add_road_spotB: 11 add_road_Length: 5669
200 add_road_K: 2
add_road_ID: 179422 add_road_spotA: 9 add_road_spotB: 18 add_road_Length: 4958
add_road_ID: 602082 add_road_spotA: 16 add_road_spotB: 12 add_road_Length: 4542
200 add_road_K: 1
add_road_ID: 571768 add_road_spotA: 25 add_road_spotB: 27 add_road_Length: 5942
200 add_road_K: 1
add_road_ID: 453402 add_road_spotA: 3 add_road_spotB: 19 add_road_Length: 5490
200 add_road_K: 1
add_road_ID: 348003 add_road_spotA: 9 add_road_spotB: 27 add_road_Length: 5722
200 add_road_K: 2
add_road_ID: 492635 add_road_spotA: 17 add_road_spotB: 11 add_road_Length: 5105
add_road_ID: 212023 add_road_spotA: 27 add_road_spotB: 17 add_road_Length: 5055
200 add_road_K: 1
add_road_ID: 167339 add_road_spotA: 8 add_road_spotB: 13 add_road_Length: 4955
200 add_road_K: 2
add_road_ID: 132746 add_road_spotA: 7 add_road_spotB: 8 add_road_Length: 5512
add_road_ID: 168520 add_road_spotA: 14 add_road_spotB: 20 add_road_Length: 5409
200 add_road_K: 2
add_road_ID: 514348 add_road_spotA: 13 add_road_spotB: 29 add_road_Length: 5680
add_road_ID: 592945 add_road_spotA: 15 add_road_spotB: 22 add_road_Length: 5417
200 add_road_K: 2
add_road_ID: 386439 add_road_spotA: 19 add_road_spotB: 15 add_road_Length: 4999
add_road_ID: 352544 add_road_spotA: 12 add_road_spotB: 30 add_road_Length: 5825
200 add_road_K: 2
add_road_ID: 585359 add_road_spotA: 8 add_road_spotB: 9 add_road_Length: 4560
add_road_ID: 355964 add_road_spotA: 15 add_road_spotB: 29 add_road_Length: 5508
200 add_road_K: 2
add_road_ID: 184176 add_road_spotA: 17 add_road_spotB: 10 add_road_Length: 4972
add_road_ID: 522016 add_road_spotA: 3 add_road_spotB: 10 add_road_Length: 5152
200 add_road_K: 1
add_road_ID: 31659 add_road_spotA: 25 add_road_spotB: 7 add_road_Length: 5904
200 add_road_K: 1
add_road_ID: 471362 add_road_spotA: 2 add_road_spotB: 6 add_road_Length: 5978
200 add_road_K: 2
add_road_ID: 573140 add_road_spotA: 3 add_road_spotB: 18 add_road_Length: 4663
add_road_ID: 79996 add_road_spotA: 1 add_road_spotB: 11 add_road_Length: 5619
200 add_road_K: 2
add_road_ID: 148741 add_road_spotA: 28 add_road_spotB: 7 add_road_Length: 4519
add_road_ID: 412574 add_road_spotA: 29 add_road_spotB: 16 add_road_Length: 4913
200 add_road_K: 2
add_road_ID: 137195 add_road_spotA: 22 add_road_spotB: 26 add_road_Length: 4723
add_road_ID: 390839 add_road_spotA: 26 add_road_spotB: 18 add_road_Length: 5840
200 add_road_K: 2
add_road_ID: 143184 add_road_spotA: 1 add_road_spotB: 26 add_road_Length: 4559
add_road_ID: 455841 add_road_spotA: 19 add_road_spotB: 10 add_road_Length: 5876
200 add_road_K: 1
add_road_ID: 115523 add_road_spotA: 1 add_road_spotB: 6 add_road_Length: 4680
400 start_spotA: 13 return_length: 41641
400 start_spotA: 16 return_length: -1
400 start_spotA: 3 return_length: 42124
400 start_spotA: 24 return_length: -1
400 start_spotA: 7 return_length: -1
200 add_road_K: 2
add_road_ID: 365175 add_road_spotA: 30 add_road_spotB: 14 add_road_Length: 5387
add_road_ID: 367311 add_road_spotA: 16 add_road_spotB: 25 add_road_Length: 5579
400 start_spotA: 29 return_length: 41641
200 add_road_K: 1
add_road_ID: 50108 add_road_spotA: 28 add_road_spotB: 22 add_road_Length: 4689
400 start_spotA: 2 return_length: -1
400 start_spotA: 18 return_length: 42124
400 start_spotA: 23 return_length: -1
400 start_spotA: 21 return_length: -1
200 add_road_K: 1
add_road_ID: 609253 add_road_spotA: 14 add_road_spotB: 21 add_road_Length: 5860
400 start_spotA: 10 return_length: 42124
200 add_road_K: 2
add_road_ID: 259126 add_road_spotA: 4 add_road_spotB: 23 add_road_Length: 4504
add_road_ID: 219184 add_road_spotA: 30 add_road_spotB: 20 add_road_Length: 5473
400 start_spotA: 13 return_length: 41641
200 add_road_K: 2
add_road_ID: 485148 add_road_spotA: 21 add_road_spotB: 20 add_road_Length: 4608
add_road_ID: 120592 add_road_spotA: 2 add_road_spotB: 21 add_road_Length: 5736
400 start_spotA: 16 return_length: -1
400 start_spotA: 24 return_length: -1
400 start_spotA: 5 return_length: -1
400 start_spotA: 18 return_length: 42124
400 start_spotA: 19 return_length: 42124
400 start_spotA: 28 return_length: -1
300 remove_road_ID: 379425
400 start_spotA: 8 return_length: 41641
400 start_spotA: 9 return_length: 41641
200 add_road_K: 2
add_road_ID: 501900 add_road_spotA: 2 add_road_spotB: 5 add_road_Length: 4879
add_road_ID: 96966 add_road_spotA: 5 add_road_spotB: 4 add_road_Length: 5928
200 add_road_K: 1
add_road_ID: 517715 add_road_spotA: 23 add_road_spotB: 6 add_road_Length: 4556
400 start_spotA: 14 return_length: -1
400 start_spotA: 25 return_length: -1
400 start_spotA: 17 return_length: 42124
400 start_spotA: 6 return_length: -1
400 start_spotA: 21 return_length: -1
400 start_spotA: 7 return_length: -1
200 add_road_K: 1
add_road_ID: 87380 add_road_spotA: 5 add_road_spotB: 28 add_road_Length: 5477
200 add_road_K: 1
add_road_ID: 4201 add_road_spotA: 23 add_road_spotB: 24 add_road_Length: 5054
200 add_road_K: 1
add_road_ID: 190244 add_road_spotA: 4 add_road_spotB: 24 add_road_Length: 5048
400 start_spotA: 22 return_length: 41712
400 start_spotA: 11 return_length: 42124
400 start_spotA: 16 return_length: -1
400 start_spotA: 21 return_length: -1
300 remove_road_ID: 148741
400 start_spotA: 11 return_length: 42124
400 start_spotA: 9 return_length: 41641
400 start_spotA: 2 return_length: -1
400 start_spotA: 6 return_length: 39116
400 start_spotA: 25 return_length: -1
400 start_spotA: 18 return_length: 42124
400 start_spotA: 7 return_length: -1
400 start_spotA: 26 return_length: 42124
400 start_spotA: 14 return_length: -1
400 start_spotA: 3 return_length: 42124
400 start_spotA: 25 return_length: -1
300 remove_road_ID: 132746
400 start_spotA: 12 return_length: -1
400 start_spotA: 20 return_length: -1
300 remove_road_ID: 412574
400 start_spotA: 7 return_length: -1
400 start_spotA: 15 return_length: 41641
400 start_spotA: 3 return_length: 42124
400 start_spotA: 12 return_length: -1
400 start_spotA: 27 return_length: -1
400 start_spotA: 1 return_length: 42124
400 start_spotA: 24 return_length: 41712
400 start_spotA: 4 return_length: 41712
400 start_spotA: 12 return_length: -1
400 start_spotA: 25 return_length: -1
400 start_spotA: 20 return_length: -1
400 start_spotA: 2 return_length: -1
400 start_spotA: 18 return_length: 42124
400 start_spotA: 10 return_length: 42124
400 start_spotA: 29 return_length: 41641
400 start_spotA: 5 return_length: 41712
400 start_spotA: 26 return_length: 42124
400 start_spotA: 14 return_length: -1
400 start_spotA: 4 return_length: 41712
400 start_spotA: 10 return_length: 42124
400 start_spotA: 12 return_length: -1
400 start_spotA: 20 return_length: -1
400 start_spotA: 29 return_length: 41641
200
100 50
200 add_road_K: 1
add_road_ID: 429539 add_road_spotA: 36 add_road_spotB: 6 add_road_Length: 5553
200 add_road_K: 2
add_road_ID: 316080 add_road_spotA: 41 add_road_spotB: 40 add_road_Length: 5371
add_road_ID: 398054 add_road_spotA: 1 add_road_spotB: 4 add_road_Length: 5580
200 add_road_K: 2
add_road_ID: 92409 add_road_spotA: 44 add_road_spotB: 17 add_road_Length: 5898
add_road_ID: 393822 add_road_spotA: 18 add_road_spotB: 26 add_road_Length: 5166
200 add_road_K: 1
add_road_ID: 354617 add_road_spotA: 48 add_road_spotB: 47 add_road_Length: 5424
200 add_road_K: 2
add_road_ID: 188405 add_road_spotA: 38 add_road_spotB: 19 add_road_Length: 5115
add_road_ID: 349377 add_road_spotA: 16 add_road_spotB: 31 add_road_Length: 4613
200 add_road_K: 2
add_road_ID: 615407 add_road_spotA: 34 add_road_spotB: 46 add_road_Length: 5141
add_road_ID: 400085 add_road_spotA: 9 add_road_spotB: 46 add_road_Length: 4688
200 add_road_K: 1
add_road_ID: 372304 add_road_spotA: 31 add_road_spotB: 10 add_road_Length: 5213
200 add_road_K: 2
add_road_ID: 162305 add_road_spotA: 6 add_road_spotB: 46 add_road_Length: 5253
add_road_ID: 542624 add_road_spotA: 10 add_road_spotB: 50 add_road_Length: 5916
200 add_road_K: 1
add_road_ID: 54955 add_road_spotA: 2 add_road_spotB: 23 add_road_Length: 5523
200 add_road_K: 1
add_road_ID: 437293 add_road_spotA: 5 add_road_spotB: 35 add_road_Length: 4585
200 add_road_K: 1
add_road_ID: 357656 add_road_spotA: 45 add_road_spotB: 39 add_road_Length: 5740
200 add_road_K: 2
add_road_ID: 173408 add_road_spotA: 31 add_road_spotB: 8 add_road_Length: 5867
add_road_ID: 67000 add_road_spotA: 36 add_road_spotB: 16 add_road_Length: 5760
200 add_road_K: 1
add_road_ID: 344793 add_road_spotA: 28 add_road_spotB: 16 add_road_Length: 4649
200 add_road_K: 1
add_road_ID: 565582 add_road_spotA: 48 add_road_spotB: 15 add_road_Length: 5605
200 add_road_K: 2
add_road_ID: 258559 add_road_spotA: 14 add_road_spotB: 32 add_road_Length: 5511
add_road_ID: 71010 add_road_spotA: 3 add_road_spotB: 19 add_road_Length: 4994
200 add_road_K: 2
add_road_ID: 580612 add_road_spotA: 9 add_road_spotB: 10 add_road_Length: 5225
add_road_ID: 418381 add_road_spotA: 43 add_road_spotB: 26 add_road_Length: 5295
200 add_road_K: 2
add_road_ID: 371952 add_road_spotA: 13 add_road_spotB: 18 add_road_Length: 5811
add_road_ID: 42102 add_road_spotA: 1 add_road_spotB: 12 add_road_Length: 5861
200 add_road_K: 2
add_road_ID: 279883 add_road_spotA: 29 add_road_spotB: 24 add_road_Length: 5931
add_road_ID: 371699 add_road_spotA: 41 add_road_spotB: 39 add_road_Length: 5231
200 add_road_K: 1
add_road_ID: 358511 add_road_spotA: 1 add_road_spotB: 21 add_road_Length: 4902
200 add_road_K: 2
add_road_ID: 266832 add_road_spotA: 43 add_road_spotB: 48 add_road_Length: 5352
add_road_ID: 308656 add_road_spotA: 44 add_road_spotB: 43 add_road_Length: 4910
200 add_road_K: 1
add_road_ID: 531593 add_road_spotA: 42 add_road_spotB: 38 add_road_Length: 5001
200 add_road_K: 1
add_road_ID: 324844 add_road_spotA: 9 add_road_spotB: 13 add_road_Length: 5433
200 add_road_K: 2
add_road_ID: 162457 add_road_spotA: 19 add_road_spotB: 41 add_road_Length: 5443
add_road_ID: 599105 add_road_spotA: 22 add_road_spotB: 26 add_road_Length: 5209
200 add_road_K: 2
add_road_ID: 547138 add_road_spotA: 39 add_road_spotB: 5 add_road_Length: 4594
add_road_ID: 271626 add_road_spotA: 7 add_road_spotB: 2 add_road_Length: 5559
200 add_road_K: 1
add_road_ID: 47228 add_road_spotA: 30 add_road_spotB: 8 add_road_Length: 4546
200 add_road_K: 2
add_road_ID: 391658 add_road_spotA: 42 add_road_spotB: 4 add_road_Length: 5003
add_road_ID: 116640 add_road_spotA: 30 add_road_spotB: 47 add_road_Length: 5309
200 add_road_K: 2
add_road_ID: 423175 add_road_spotA: 42 add_road_spotB: 18 add_road_Length: 5548
add_road_ID: 24005 add_road_spotA: 30 add_road_spotB: 29 add_road_Length: 5610
200 add_road_K: 1
add_road_ID: 125870 add_road_spotA: 47 add_road_spotB: 13 add_road_Length: 5409
200 add_road_K: 1
add_road_ID: 349595 add_road_spotA: 29 add_road_spotB: 11 add_road_Length: 5103
200 add_road_K: 2
add_road_ID: 203510 add_road_spotA: 5 add_road_spotB: 20 add_road_Length: 5431
add_road_ID: 373868 add_road_spotA: 15 add_road_spotB: 33 add_road_Length: 5207
200 add_road_K: 1
add_road_ID: 28477 add_road_spotA: 40 add_road_spotB: 3 add_road_Length: 4755
200 add_road_K: 2
add_road_ID: 365104 add_road_spotA: 17 add_road_spotB: 27 add_road_Length: 4778
add_road_ID: 272428 add_road_spotA: 33 add_road_spotB: 21 add_road_Length: 4603
200 add_road_K: 2
add_road_ID: 376297 add_road_spotA: 2 add_road_spotB: 44 add_road_Length: 5155
add_road_ID: 289778 add_road_spotA: 36 add_road_spotB: 3 add_road_Length: 4974
400 start_spotA: 10 return_length: -1
400 start_spotA: 20 return_length: -1
200 add_road_K: 1
add_road_ID: 615750 add_road_spotA: 14 add_road_spotB: 8 add_road_Length: 5303
400 start_spotA: 33 return_length: -1
400 start_spotA: 37 return_length: -1
200 add_road_K: 2
add_road_ID: 68357 add_road_spotA: 49 add_road_spotB: 34 add_road_Length: 4929
add_road_ID: 111299 add_road_spotA: 4 add_road_spotB: 37 add_road_Length: 4902
200 add_road_K: 1
add_road_ID: 28850 add_road_spotA: 23 add_road_spotB: 7 add_road_Length: 4615
300 remove_road_ID: 542624
200 add_road_K: 2
add_road_ID: 392802 add_road_spotA: 11 add_road_spotB: 15 add_road_Length: 5062
add_road_ID: 407238 add_road_spotA: 28 add_road_spotB: 33 add_road_Length: 5250
400 start_spotA: 11 return_length: -1
400 start_spotA: 5 return_length: -1
200 add_road_K: 2
add_road_ID: 348675 add_road_spotA: 50 add_road_spotB: 27 add_road_Length: 5135
add_road_ID: 277960 add_road_spotA: 38 add_road_spotB: 34 add_road_Length: 4556
400 start_spotA: 32 return_length: -1
400 start_spotA: 50 return_length: -1
400 start_spotA: 46 return_length: -1
400 start_spotA: 30 return_length: -1
400 start_spotA: 15 return_length: -1
200 add_road_K: 1
add_road_ID: 279988 add_road_spotA: 22 add_road_spotB: 21 add_road_Length: 5814
400 start_spotA: 50 return_length: -1
400 start_spotA: 36 return_length: -1
400 start_spotA: 30 return_length: -1
200 add_road_K: 2
add_road_ID: 220887 add_road_spotA: 6 add_road_spotB: 28 add_road_Length: 4977
add_road_ID: 75426 add_road_spotA: 50 add_road_spotB: 24 add_road_Length: 5251
400 start_spotA: 42 return_length: -1
400 start_spotA: 46 return_length: -1
400 start_spotA: 3 return_length: -1
400 start_spotA: 6 return_length: -1
400 start_spotA: 23 return_length: -1
400 start_spotA: 15 return_length: -1
400 start_spotA: 20 return_length: -1
200 add_road_K: 2
add_road_ID: 185310 add_road_spotA: 14 add_road_spotB: 25 add_road_Length: 4683
add_road_ID: 508945 add_road_spotA: 22 add_road_spotB: 27 add_road_Length: 4627
200 add_road_K: 2
add_road_ID: 288486 add_road_spotA: 12 add_road_spotB: 32 add_road_Length: 5426
add_road_ID: 473179 add_road_spotA: 20 add_road_spotB: 23 add_road_Length: 4904
400 start_spotA: 25 return_length: -1
200 add_road_K: 2
add_road_ID: 488189 add_road_spotA: 17 add_road_spotB: 11 add_road_Length: 5175
add_road_ID: 467267 add_road_spotA: 20 add_road_spotB: 25 add_road_Length: 5492
400 start_spotA: 10 return_length: -1
400 start_spotA: 20 return_length: -1
400 start_spotA: 37 return_length: -1
400 start_spotA: 6 return_length: -1
400 start_spotA: 45 return_length: -1
400 start_spotA: 38 return_length: -1
200 add_road_K: 2
add_road_ID: 50904 add_road_spotA: 45 add_road_spotB: 40 add_road_Length: 4991
add_road_ID: 38803 add_road_spotA: 32 add_road_spotB: 37 add_road_Length: 5579
400 start_spotA: 18 return_length: -1
200 add_road_K: 1
add_road_ID: 394351 add_road_spotA: 7 add_road_spotB: 35 add_road_Length: 5084
200 add_road_K: 1
add_road_ID: 38169 add_road_spotA: 12 add_road_spotB: 24 add_road_Length: 5253
200 add_road_K: 1
add_road_ID: 321678 add_road_spotA: 25 add_road_spotB: 35 add_road_Length: 4804
400 start_spotA: 41 return_length: -1
400 start_spotA: 12 return_length: 41922
200 add_road_K: 1
add_road_ID: 165989 add_road_spotA: 37 add_road_spotB: 45 add_road_Length: 5974
400 start_spotA: 11 return_length: 41922
400 start_spotA: 47 return_length: -1
300 remove_road_ID: 24005
400 start_spotA: 44 return_length: -1
400 start_spotA: 15 return_length: 41922
400 start_spotA: 26 return_length: 41103
400 start_spotA: 1 return_length: 41922
400 start_spotA: 11 return_length: 41922
300 remove_road_ID: 398054
400 start_spotA: 34 return_length: -1
300 remove_road_ID: 358511
300 remove_road_ID: 38169
400 start_spotA: 22 return_length: 41103
400 start_spotA: 32 return_length: 41470
400 start_spotA: 32 return_length: 41470
400 start_spotA: 25 return_length: 41470
400 start_spotA: 33 return_length: -1
400 start_spotA: 7 return_length: -1
400 start_spotA: 40 return_length: 41800
400 start_spotA: 33 return_length: -1
400 start_spotA: 43 return_length: 41103
400 start_spotA: 31 return_length: -1
400 start_spotA: 6 return_length: -1
400 start_spotA: 38 return_length: 41800
400 start_spotA: 41 return_length: 41800
400 start_spotA: 7 return_length: -1
400 start_spotA: 29 return_length: -1
400 start_spotA: 25 return_length: 41470
400 start_spotA: 41 return_length: 41800
400 start_spotA: 41 return_length: 41800
300 remove_road_ID: 288486
400 start_spotA: 19 return_length: 41800
400 start_spotA: 23 return_length: -1
400 start_spotA: 47 return_length: -1
400 start_spotA: 22 return_length: 41103
400 start_spotA: 11 return_length: 41103
400 start_spotA: 29 return_length: -1
400 start_spotA: 25 return_length: 41470
400 start_spotA: 50 return_length: -1
400 start_spotA: 11 return_length: 41103
400 start_spotA: 43 return_length: 41103
400 start_spotA: 28 return_length: -1
400 start_spotA: 47 return_length: -1
400 start_spotA: 46 return_length: -1
400 start_spotA: 41 return_length: 41800
400 start_spotA: 44 return_length: -1
400 start_spotA: 34 return_length: -1
400 start_spotA: 10 return_length: -1
400 start_spotA: 2 return_length: -1
400 start_spotA: 35 return_length: 41470
400 start_spotA: 45 return_length: 41800
400 start_spotA: 24 return_length: -1
400 start_spotA: 14 return_length: 41470
400 start_spotA: 24 return_length: -1
400 start_spotA: 14 return_length: 41470
400 start_spotA: 17 return_length: 41103
400 start_spotA: 4 return_length: 41800
400 start_spotA: 32 return_length: 41470
400 start_spotA: 21 return_length: -1
300 remove_road_ID: 28850
400 start_spotA: 1 return_length: -1
400 start_spotA: 19 return_length: 41800
400 start_spotA: 2 return_length: -1
400 start_spotA: 12 return_length: -1
400 start_spotA: 27 return_length: 41103
400 start_spotA: 7 return_length: -1
400 start_spotA: 21 return_length: -1
400 start_spotA: 17 return_length: 41103
400 start_spotA: 14 return_length: 41470
400 start_spotA: 8 return_length: -1
400 start_spotA: 23 return_length: -1
400 start_spotA: 30 return_length: -1
400 start_spotA: 44 return_length: -1
400 start_spotA: 19 return_length: 41800
400 start_spotA: 28 return_length: -1
400 start_spotA: 30 return_length: -1
400 start_spotA: 39 return_length: 41470
400 start_spotA: 16 return_length: -1
400 start_spotA: 11 return_length: 41103
400 start_spotA: 34 return_length: -1
400 start_spotA: 49 return_length: -1
400 start_spo
출력:
#1 100
#2 100
#3 100
#4 100
#5 100
#6 100
#7 100
#8 100
#9 100
#10 100
#11 100
#12 100
#13 100
#14 100
#15 100
#16 100
#17 100
#18 100
#19 100
#20 100
#21 100
#22 100
#23 100
#24 100
#25 100
"""

# ── User Code ──
from typing import List
from collections import defaultdict


# n 은 10 이상 1000 이하.
def init(N: int) -> None:
    global g_N, roads, graph
    g_N = N
    roads = defaultdict(list)
    graph = [set() for _ in range(N + 1)]
    pass

# 하나의 지점에 연결되는 도로는 최대 5개
# 1000
def addRoad(K: int, mID: List[int], mSpotA: List[int], mSpotB: List[int], mLen: List[int]) -> None:

    for k in range(K):
        roads[mID[k]] = [
            mSpotA[k],
            mSpotB[k],
            mLen[k],
            True
        ]

        graph[mSpotA[k]].add(mID[k])
        graph[mSpotB[k]].add(mID[k])

# 100
def removeRoad(mID: int) -> None:
    roads[mID][3] = False

def dfs(start, cur, depth, length, used_edges):

    if depth == 4:
        paths[cur].append((length, frozenset(used_edges)))
        return

    # 다음 방문처 확인
    for nxt_road_id in graph[cur]:
        if nxt_road_id in used_edges:
            continue

        spota, spotb, mlen, is_ok = roads[nxt_road_id]

        if not is_ok:
            continue

        new_length = length + mlen

        if new_length > 42195:
            continue

        if spota == cur:
            #spot b 로 움직이기
            if start == spotb:
                continue
            used_edges.append(nxt_road_id)
            dfs(start, spotb, depth + 1, new_length, used_edges)
        else:
            if start == spota:
                continue
            used_edges.append(nxt_road_id)
            dfs(start, spota, depth + 1, new_length, used_edges)

        used_edges.pop()

# 1000
def getLength(mSpot: int) -> int:
    global paths
    paths = [[] for _ in range(g_N + 1)]
    dfs(mSpot, mSpot, 0, 0, [])
    answer = -1
    for spot in range(1, g_N + 1):
        if spot == mSpot:
            continue
        cur_paths = paths[spot]

        for i in range(len(cur_paths)):
            len1, edges1 = cur_paths[i]

            for j in range(i + 1, len(cur_paths)):
                len2, edges2 = cur_paths[j]

                total = len1 + len2

                if total > 42195:
                    continue

                if not edges1.isdisjoint(edges2):
                    continue

                answer = max(answer, total)
    # print("getlength", answer)
    return answer


# ── Main (수정 불가) ──
import sys
# (합쳐서 실행하므로 import 제거)

CMD_INIT = 100
CMD_ADD = 200
CMD_REMOVE = 300
CMD_GETLEN = 400

rid = [0 for _ in range(10)]
sa = [0 for _ in range(10)]
sb = [0 for _ in range(10)]
length = [0 for _ in range(10)]

def run():
    global rid, sa, sb, length
    Q = int(input())
    okay = False
    for q in range(Q):
        input_iter = iter(input().split())
        cmd = int(next(input_iter))
        if cmd == CMD_INIT:
            n = int(next(input_iter))
            init(n)
            okay = True
        elif cmd == CMD_ADD:
            strTmp = next(input_iter)
            k = int(next(input_iter))
            for i in range(k):
                in_iter = iter(input().split())
                strTmp = next(in_iter)
                rid[i] = int(next(in_iter))
                strTmp = next(in_iter)
                sa[i] = int(next(in_iter))
                strTmp = next(in_iter)
                sb[i] = int(next(in_iter))
                strTmp = next(in_iter)
                length[i] = int(next(in_iter))
            addRoad(k, rid, sa, sb, length)
        elif cmd == CMD_REMOVE:
            strTmp = next(input_iter)
            mid = int(next(input_iter))
            removeRoad(mid)
        elif cmd == CMD_GETLEN:
            strTmp = next(input_iter)
            mid = int(next(input_iter))
            ret = getLength(mid)
            strTmp = next(input_iter)
            ans = int(next(input_iter))
            if ret != ans:
                okay = False
        else:
            okay = False
    return okay


#sys.stdin = open('sample_input.txt', 'r')

T, MARK = map(int, input().split())

for tc in range(1, T + 1):
    score = MARK if run() else 0
    print("#%d %d" % (tc, score), flush = True)
