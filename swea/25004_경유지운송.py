"""
SWEA 25004  경유지운송
https://swexpertacademy.com/main/talk/solvingClub/problemView.do?solveclubId=AZt8IiBqxEDHBIN6&contestProbId=AZih4lcKvKDHBINp&probBoxId=AZt8IiBqxEHHBIN6&type=PROBLEM

풀이일 : 2026-08-28   결과: 시간초과
한도   : time 25개 테스트케이스를 합쳐서 C++의 경우 3초 / Java의 경우 3초 / Python의 경우 6.5초 / memory 힙, 정적 메모리 합쳐서 262144 kbytes 이내, 스택 메모리 1024 kbytes 이내 / time_sec 6.5
난이도 : D6  |  정답률 94.34%
제약   : 1. 각 테스트 케이스 시작 시 init() 함수가 호출된다.
제약   : 2. 각 테스트 케이스에서 add() 함수의 호출 횟수는 1,400 이하이다.
제약   : 3. 각 테스트 케이스에서 calculate() 함수의 호출 횟수는 100 이하이다.

[채점] accepted  1/1  (3.524s)

[문제]
N개의 도시가 주어진다. 각 도시는 0부터 N-1까지 ID값을 가진다.

도시를 연결하는 양방향 도로가 추가될 때, 해당 도로를 이용할 수 있는 최대 중량이 주어진다.

출발 도시와 도착 도시, 그리고 경유지가 주어졌을 때, 운송할 수 있는 화물의 최대 중량을 구하고자 한다.

경유지는 최대 3개 주어지며, 순서에 상관 없이 방문하면 된다. 동일한 경유지를 여러 번 방문할 수 있고,

경유지를 방문하기 위해 출발 도시나 도착 도시를 거쳐서 가도 된다.

[Fig. 1]은 5개의 도시가 주어진 예이다.

[[IMG:1]]

[Fig. 1]

경유지가 1번, 3번 도시일 때, 0번 도시에서 4번 도시로 운송할 수 있는 화물의 최대 중량은 60이다.

(0 --(limit:80)--> 2 --(limit:70)--> 1 --(limit:60)--> 3 --(limit:60)--> 1 --(limit:90)--> 4)

아래 API 설명을 참조하여 각 함수를 구현하라.

※ 아래 함수 signature는 C/C++에 대한 것으로 다른 언어에 대해서는 제공되는 Main과 User Code를 참고하라.

아래는 User Code 부분에 작성해야 하는 API 의 설명이다.

void init(int N, int K, int sCity[], int eCity[], int mLimit[])

각 테스트 케이스의 처음에 호출된다.

N개의 도시가 주어진다. 각 도시는 0부터 N-1까지 ID값을 가진다.

K개의 양방향 도로 정보가 주어진다. 각 도로마다 연결된 2개의 도시와 도로를 이용할 수 있는 최대 중량이 주어진다.

2개의 도시를 연결하는 도로는 1개만 주어진다.

도로와 연결된 2개의 도시가 서로 같은 경우는 없다.

Parameters

N: 도시의 개수 ( 5 ≤ N ≤ 1,000 )

K: 도로의 개수 ( 2 ≤ K ≤ 2,000 )

(0 ≤ i ＜ K)인 모든 i에 대해,

sCity[i]: 도로 i와 연결된 도시 ( 0 ≤ sCity[i] < N )

eCity[i]: 도로 i와 연결된 도시 ( 0 ≤ eCity[i] < N )

mLimit[i]: 도로 i를 이용할 수 있는 최대 중량 ( 1 ≤ mLimit[i] ≤ 30,000 )

void add(int sCity, int eCity, int mLimit)

sCity 도시와 eCity 도시를 연결하는 양방향 도로를 추가한다.

도로를 이용할 수 있는 최대 중량은 mLimit이다.

init()에 없던 새로운 도시는 주어지지 않는다.

sCity와 eCity를 연결하는 도로가 이미 존재하는 경우는 없다.

sCity와 eCity가 서로 같은 경우는 없다.

Parameters

sCity: 도로와 연결된 도시 ( 0 ≤ sCity < N )

eCity: 도로와 연결된 도시 ( 0 ≤ eCity < N )

mLimit: 도로를 이용할 수 있는 최대 중량 ( 1 ≤ mLimit ≤ 30,000 )

int calculate(int sCity, int eCity, int M, int mStopover[])

M개의 경유지가 mStopover 배열로 주어진다.

sCity에서 M개의 경유지를 거쳐서 eCity까지 운송할 수 있는 화물의 최대 중량을 반환한다.

sCity와 eCity가 서로 같은 경우는 없다.

M개의 경유지가 서로 같은 경우는 없다.

경유지가 sCity나 eCity와 동일한 경우는 없다.

Parameters

sCity: 출발 도시 ( 0 ≤ sCity < N )

eCity: 도착 도시 ( 0 ≤ eCity < N )

M: 경유지 개수 ( 1 ≤ M ≤ 3)

(0 ≤ i ＜ M)인 모든 i에 대해,

mStopover[i]: 경유해야 되는 도시 ( 0 ≤ mStopover[i] < N )

Returns

sCity에서 M개의 경유지를 거쳐서 eCity까지 이동이 가능하다면, 운송할 수 있는 화물의 최대 중량을 반환한다.

불가능하다면, -1을 반환한다.

[예제 1]
입력:
25 100
11
100 CMD_INIT
 number_of_city: 5  number_of_road: 2
 city_id:   0  city_id:   1  limit: 50
 city_id:   1  city_id:   4  limit: 90
300 CMD_CALC
 sender_city_id:   1  receiver_city_id:   4  number_of_stopover: 1
 stopover_city_id: 3
 answer: -1
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   4  number_of_stopover: 1
 stopover_city_id: 1
 answer: 50
200 CMD_ADD
 city_id:   3  city_id:   4  limit: 30
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   4  number_of_stopover: 1
 stopover_city_id: 3
 answer: 30
200 CMD_ADD
 city_id:   3  city_id:   1  limit: 60
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   4  number_of_stopover: 2
 stopover_city_id: 3
 stopover_city_id: 1
 answer: 50
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   4  number_of_stopover: 3
 stopover_city_id: 2
 stopover_city_id: 3
 stopover_city_id: 1
 answer: -1
200 CMD_ADD
 city_id:   0  city_id:   2  limit: 80
200 CMD_ADD
 city_id:   2  city_id:   1  limit: 70
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   4  number_of_stopover: 3
 stopover_city_id: 2
 stopover_city_id: 3
 stopover_city_id: 1
 answer: 60
30
100 CMD_INIT
 number_of_city: 20  number_of_road: 10
 city_id:   8  city_id:  19  limit: 6930
 city_id:  17  city_id:   1  limit: 18423
 city_id:   1  city_id:   0  limit: 4552
 city_id:   0  city_id:   4  limit: 4677
 city_id:   4  city_id:  14  limit: 26110
 city_id:  14  city_id:   6  limit: 24003
 city_id:  10  city_id:   8  limit: 24020
 city_id:   7  city_id:  17  limit: 15713
 city_id:  11  city_id:  18  limit: 12042
 city_id:  18  city_id:  10  limit: 18431
200 CMD_ADD
 city_id:  10  city_id:  15  limit: 29805
200 CMD_ADD
 city_id:  14  city_id:   3  limit: 14633
200 CMD_ADD
 city_id:   4  city_id:   1  limit: 5363
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:   5  number_of_stopover: 1
 stopover_city_id: 3
 answer: -1
200 CMD_ADD
 city_id:  17  city_id:   6  limit: 11244
200 CMD_ADD
 city_id:   1  city_id:  10  limit: 5384
200 CMD_ADD
 city_id:   1  city_id:  18  limit: 10676
200 CMD_ADD
 city_id:   1  city_id:   6  limit: 11792
200 CMD_ADD
 city_id:   5  city_id:  10  limit: 5676
200 CMD_ADD
 city_id:  17  city_id:   2  limit: 23352
200 CMD_ADD
 city_id:  17  city_id:  14  limit: 22836
200 CMD_ADD
 city_id:  13  city_id:   6  limit: 6764
200 CMD_ADD
 city_id:  15  city_id:   0  limit: 26750
200 CMD_ADD
 city_id:  11  city_id:   0  limit: 11146
300 CMD_CALC
 sender_city_id:  19  receiver_city_id:   4  number_of_stopover: 2
 stopover_city_id: 10
 stopover_city_id: 15
 answer: 6930
200 CMD_ADD
 city_id:   5  city_id:  14  limit: 11304
200 CMD_ADD
 city_id:  19  city_id:  16  limit: 7338
200 CMD_ADD
 city_id:   3  city_id:  12  limit: 8342
200 CMD_ADD
 city_id:  19  city_id:   4  limit: 11282
200 CMD_ADD
 city_id:   3  city_id:  16  limit: 11614
200 CMD_ADD
 city_id:   7  city_id:  16  limit: 25274
200 CMD_ADD
 city_id:   1  city_id:  14  limit: 4892
200 CMD_ADD
 city_id:   9  city_id:  10  limit: 10052
200 CMD_ADD
 city_id:   9  city_id:  18  limit: 27296
200 CMD_ADD
 city_id:  19  city_id:  12  limit: 10002
200 CMD_ADD
 city_id:  11  city_id:   8  limit: 9406
200 CMD_ADD
 city_id:   9  city_id:   6  limit: 21068
200 CMD_ADD
 city_id:   5  city_id:  18  limit: 8136
300 CMD_CALC
 sender_city_id:   9  receiver_city_id:  10  number_of_stopover: 3
 stopover_city_id: 8
 stopover_city_id: 13
 stopover_city_id: 6
 answer: 6764
50
100 CMD_INIT
 number_of_city: 30  number_of_road: 20
 city_id:   4  city_id:   5  limit: 22356
 city_id:   7  city_id:  19  limit: 7185
 city_id:   2  city_id:   3  limit: 394
 city_id:  15  city_id:  22  limit: 6335
 city_id:   5  city_id:   8  limit: 14000
 city_id:  25  city_id:   1  limit: 29389
 city_id:   0  city_id:  17  limit: 18694
 city_id:  13  city_id:  16  limit: 2155
 city_id:  17  city_id:  15  limit: 22924
 city_id:  19  city_id:  13  limit: 12425
 city_id:  11  city_id:   7  limit: 25618
 city_id:  20  city_id:   9  limit: 28247
 city_id:  23  city_id:  27  limit: 26776
 city_id:  27  city_id:  14  limit: 8853
 city_id:  14  city_id:  26  limit: 10334
 city_id:  26  city_id:   0  limit: 18323
 city_id:   9  city_id:  10  limit: 18772
 city_id:   8  city_id:  11  limit: 26849
 city_id:  12  city_id:  28  limit: 490
 city_id:  22  city_id:  21  limit: 3759
200 CMD_ADD
 city_id:   4  city_id:  17  limit: 921
200 CMD_ADD
 city_id:   4  city_id:  19  limit: 3061
200 CMD_ADD
 city_id:   6  city_id:   7  limit: 29233
200 CMD_ADD
 city_id:  16  city_id:  19  limit: 8589
200 CMD_ADD
 city_id:  22  city_id:  23  limit: 13017
200 CMD_ADD
 city_id:   6  city_id:  27  limit: 5413
200 CMD_ADD
 city_id:  18  city_id:  27  limit: 4769
300 CMD_CALC
 sender_city_id:  26  receiver_city_id:   3  number_of_stopover: 1
 stopover_city_id: 5
 answer: -1
200 CMD_ADD
 city_id:  23  city_id:   6  limit: 4402
200 CMD_ADD
 city_id:  13  city_id:   0  limit: 10590
200 CMD_ADD
 city_id:  23  city_id:  20  limit: 28810
200 CMD_ADD
 city_id:   7  city_id:  22  limit: 15878
200 CMD_ADD
 city_id:   7  city_id:  12  limit: 19938
200 CMD_ADD
 city_id:  23  city_id:  24  limit: 622
200 CMD_ADD
 city_id:  13  city_id:   8  limit: 15418
200 CMD_ADD
 city_id:  17  city_id:  20  limit: 4134
200 CMD_ADD
 city_id:  11  city_id:  28  limit: 7314
200 CMD_ADD
 city_id:  13  city_id:  18  limit: 6030
200 CMD_ADD
 city_id:   1  city_id:  20  limit: 208
200 CMD_ADD
 city_id:  17  city_id:  24  limit: 17148
200 CMD_ADD
 city_id:  27  city_id:  12  limit: 1816
200 CMD_ADD
 city_id:  23  city_id:  14  limit: 20388
200 CMD_ADD
 city_id:   7  city_id:  14  limit: 23824
200 CMD_ADD
 city_id:  27  city_id:  26  limit: 29778
200 CMD_ADD
 city_id:  17  city_id:  12  limit: 17486
200 CMD_ADD
 city_id:  25  city_id:   2  limit: 18778
200 CMD_ADD
 city_id:   5  city_id:  24  limit: 28486
200 CMD_ADD
 city_id:  19  city_id:  20  limit: 27218
200 CMD_ADD
 city_id:  11  city_id:  14  limit: 3566
200 CMD_ADD
 city_id:   5  city_id:   2  limit: 7050
200 CMD_ADD
 city_id:  27  city_id:  24  limit: 22924
200 CMD_ADD
 city_id:  11  city_id:   2  limit: 10632
200 CMD_ADD
 city_id:  19  city_id:   2  limit: 3924
300 CMD_CALC
 sender_city_id:   5  receiver_city_id:   6  number_of_stopover: 3
 stopover_city_id: 28
 stopover_city_id: 25
 stopover_city_id: 14
 answer: 7314
200 CMD_ADD
 city_id:  24  city_id:  15  limit: 23863
300 CMD_CALC
 sender_city_id:   4  receiver_city_id:  27  number_of_stopover: 3
 stopover_city_id: 29
 stopover_city_id: 2
 stopover_city_id: 13
 answer: -1
200 CMD_ADD
 city_id:  17  city_id:   6  limit: 6550
200 CMD_ADD
 city_id:   9  city_id:   2  limit: 14360
200 CMD_ADD
 city_id:  21  city_id:  18  limit: 9588
200 CMD_ADD
 city_id:  25  city_id:  16  limit: 8332
200 CMD_ADD
 city_id:   7  city_id:   2  limit: 26856
200 CMD_ADD
 city_id:  19  city_id:   8  limit: 7716
200 CMD_ADD
 city_id:  15  city_id:   6  limit: 2950
200 CMD_ADD
 city_id:   1  city_id:  24  limit: 27394
300 CMD_CALC
 sender_city_id:   1  receiver_city_id:   8  number_of_stopover: 2
 stopover_city_id: 6
 stopover_city_id: 3
 answer: 394
200 CMD_ADD
 city_id:   7  city_id:   0  limit: 15168
300 CMD_CALC
 sender_city_id:   1  receiver_city_id:  18  number_of_stopover: 1
 stopover_city_id: 12
 answer: 6030
300 CMD_CALC
 sender_city_id:  20  receiver_city_id:   3  number_of_stopover: 3
 stopover_city_id: 29
 stopover_city_id: 14
 stopover_city_id: 27
 answer: -1
300 CMD_CALC
 sender_city_id:  11  receiver_city_id:   8  number_of_stopover: 1
 stopover_city_id: 28
 answer: 7314
50
100 CMD_INIT
 number_of_city: 30  number_of_road: 20
 city_id:  21  city_id:  12  limit: 19754
 city_id:  12  city_id:  28  limit: 28239
 city_id:  15  city_id:   9  limit: 21280
 city_id:  25  city_id:  10  limit: 23469
 city_id:  10  city_id:   0  limit: 4438
 city_id:   1  city_id:   6  limit: 12779
 city_id:   6  city_id:  16  limit: 21724
 city_id:  26  city_id:   2  limit: 8553
 city_id:  27  city_id:  25  limit: 15714
 city_id:  19  city_id:  11  limit: 28231
 city_id:  29  city_id:  14  limit: 23384
 city_id:  20  city_id:   4  limit: 11333
 city_id:   8  city_id:   1  limit: 25374
 city_id:  18  city_id:  20  limit: 3571
 city_id:  23  city_id:   3  limit: 25636
 city_id:  14  city_id:  18  limit: 1985
 city_id:   9  city_id:   8  limit: 15162
 city_id:   2  city_id:  21  limit: 8767
 city_id:  17  city_id:  22  limit: 19200
 city_id:   4  city_id:  26  limit: 19357
200 CMD_ADD
 city_id:  24  city_id:  11  limit: 27831
200 CMD_ADD
 city_id:  22  city_id:  21  limit: 10611
200 CMD_ADD
 city_id:   6  city_id:   3  limit: 7487
200 CMD_ADD
 city_id:   4  city_id:   1  limit: 1131
300 CMD_CALC
 sender_city_id:  26  receiver_city_id:  15  number_of_stopover: 1
 stopover_city_id: 5
 answer: -1
200 CMD_ADD
 city_id:  29  city_id:  12  limit: 28612
200 CMD_ADD
 city_id:  27  city_id:  14  limit: 4064
200 CMD_ADD
 city_id:  13  city_id:  12  limit: 5644
200 CMD_ADD
 city_id:   5  city_id:  22  limit: 15912
300 CMD_CALC
 sender_city_id:   7  receiver_city_id:  22  number_of_stopover: 1
 stopover_city_id: 0
 answer: -1
200 CMD_ADD
 city_id:  20  city_id:  19  limit: 22205
200 CMD_ADD
 city_id:  28  city_id:  23  limit: 3881
200 CMD_ADD
 city_id:   2  city_id:   3  limit: 1381
200 CMD_ADD
 city_id:  12  city_id:   5  limit: 2641
200 CMD_ADD
 city_id:  18  city_id:  29  limit: 7357
200 CMD_ADD
 city_id:   8  city_id:  25  limit: 14617
200 CMD_ADD
 city_id:   4  city_id:  19  limit: 23317
200 CMD_ADD
 city_id:  20  city_id:   5  limit: 22079
200 CMD_ADD
 city_id:  20  city_id:  27  limit: 24811
200 CMD_ADD
 city_id:  14  city_id:  17  limit: 2773
200 CMD_ADD
 city_id:  22  city_id:   9  limit: 27473
200 CMD_ADD
 city_id:   2  city_id:  25  limit: 21853
200 CMD_ADD
 city_id:  12  city_id:  25  limit: 8409
300 CMD_CALC
 sender_city_id:  18  receiver_city_id:  15  number_of_stopover: 3
 stopover_city_id: 7
 stopover_city_id: 16
 stopover_city_id: 25
 answer: -1
200 CMD_ADD
 city_id:  27  city_id:  10  limit: 12672
200 CMD_ADD
 city_id:   7  city_id:   8  limit: 7692
200 CMD_ADD
 city_id:  15  city_id:  18  limit: 4872
200 CMD_ADD
 city_id:  15  city_id:   4  limit: 25460
200 CMD_ADD
 city_id:   5  city_id:   8  limit: 14672
200 CMD_ADD
 city_id:   3  city_id:  16  limit: 15324
200 CMD_ADD
 city_id:  27  city_id:  12  limit: 408
200 CMD_ADD
 city_id:  21  city_id:   0  limit: 10308
200 CMD_ADD
 city_id:  25  city_id:  28  limit: 1360
200 CMD_ADD
 city_id:  29  city_id:   2  limit: 26732
200 CMD_ADD
 city_id:  25  city_id:  14  limit: 23624
200 CMD_ADD
 city_id:  19  city_id:   0  limit: 10596
200 CMD_ADD
 city_id:   9  city_id:  26  limit: 23360
200 CMD_ADD
 city_id:   1  city_id:  24  limit: 27842
300 CMD_CALC
 sender_city_id:  23  receiver_city_id:  26  number_of_stopover: 3
 stopover_city_id: 22
 stopover_city_id: 0
 stopover_city_id: 13
 answer: 5644
200 CMD_ADD
 city_id:  19  city_id:  28  limit: 25510
200 CMD_ADD
 city_id:  15  city_id:  24  limit: 6146
200 CMD_ADD
 city_id:  21  city_id:   4  limit: 23470
200 CMD_ADD
 city_id:  17  city_id:   6  limit: 9882
200 CMD_ADD
 city_id:  23  city_id:   0  limit: 27206
200 CMD_ADD
 city_id:  13  city_id:  10  limit: 17730
200 CMD_ADD
 city_id:   1  city_id:  28  limit: 28394
200 CMD_ADD
 city_id:   5  city_id:  24  limit: 19228
200 CMD_ADD
 city_id:  13  city_id:  26  limit: 2494
300 CMD_CALC
 sender_city_id:  13  receiver_city_id:   2  number_of_stopover: 2
 stopover_city_id: 12
 stopover_city_id: 3
 answer: 12779
100
100 CMD_INIT
 number_of_city: 40  number_of_road: 50
 city_id:   9  city_id:  19  limit: 24333
 city_id:   8  city_id:   1  limit: 21350
 city_id:  19  city_id:  11  limit: 27531
 city_id:  35  city_id:  18  limit: 27420
 city_id:  36  city_id:  23  limit: 19689
 city_id:  29  city_id:  20  limit: 11858
 city_id:  39  city_id:  25  limit: 295
 city_id:  22  city_id:  39  limit: 14760
 city_id:  32  city_id:  34  limit: 1157
 city_id:  33  city_id:  32  limit: 23070
 city_id:  10  city_id:   3  limit: 20995
 city_id:  11  city_id:  37  limit: 12308
 city_id:  20  city_id:  15  limit: 513
 city_id:  21  city_id:   6  limit: 6922
 city_id:  38  city_id:  31  limit: 15279
 city_id:  15  city_id:  14  limit: 16880
 city_id:  24  city_id:   2  limit: 12973
 city_id:  16  city_id:   9  limit: 2310
 city_id:   3  city_id:  29  limit: 6587
 city_id:   2  city_id:  26  limit: 3564
 city_id:   4  city_id:  21  limit: 2953
 city_id:   5  city_id:  22  limit: 9282
 city_id:  31  city_id:  16  limit: 8983
 city_id:   7  city_id:   8  limit: 5416
 city_id:   1  city_id:  10  limit: 10853
 city_id:  17  city_id:  35  limit: 9166
 city_id:  26  city_id:   4  limit: 21827
 city_id:  27  city_id:  12  limit: 3140
 city_id:  37  city_id:   5  limit: 4785
 city_id:  13  city_id:  36  limit: 24474
 city_id:   6  city_id:   7  limit: 29551
 city_id:  23  city_id:  30  limit: 16176
 city_id:  25  city_id:  24  limit: 7197
 city_id:   0  city_id:  17  limit: 10598
 city_id:  18  city_id:  13  limit: 29227
 city_id:  34  city_id:  27  limit: 23340
 city_id:  12  city_id:  28  limit: 25977
 city_id:  28  city_id:  38  limit: 20562
 city_id:  30  city_id:  33  limit: 14599
 city_id:  14  city_id:   0  limit: 11608
 city_id:  36  city_id:   5  limit: 13731
 city_id:  11  city_id:  32  limit: 13002
 city_id:  38  city_id:  23  limit: 2125
 city_id:  29  city_id:  18  limit: 10380
 city_id:  32  city_id:  17  limit: 28903
 city_id:  39  city_id:  12  limit: 2126
 city_id:  10  city_id:  35  limit: 20017
 city_id:  25  city_id:  14  limit: 18624
 city_id:  28  city_id:  37  limit: 23211
 city_id:   3  city_id:  16  limit: 19058
200 CMD_ADD
 city_id:  35  city_id:  24  limit: 27626
200 CMD_ADD
 city_id:  31  city_id:  28  limit: 19078
200 CMD_ADD
 city_id:  27  city_id:   0  limit: 13986
200 CMD_ADD
 city_id:  15  city_id:  12  limit: 5678
200 CMD_ADD
 city_id:  27  city_id:  32  limit: 890
200 CMD_ADD
 city_id:   7  city_id:  36  limit: 24822
300 CMD_CALC
 sender_city_id:  11  receiver_city_id:   0  number_of_stopover: 1
 stopover_city_id: 30
 answer: 10598
200 CMD_ADD
 city_id:  36  city_id:  37  limit: 21747
200 CMD_ADD
 city_id:  24  city_id:  33  limit: 20639
200 CMD_ADD
 city_id:   8  city_id:  25  limit: 29287
200 CMD_ADD
 city_id:  20  city_id:  37  limit: 18099
300 CMD_CALC
 sender_city_id:   8  receiver_city_id:  17  number_of_stopover: 2
 stopover_city_id: 23
 stopover_city_id: 28
 answer: 10853
200 CMD_ADD
 city_id:  16  city_id:  17  limit: 3287
200 CMD_ADD
 city_id:  28  city_id:  21  limit: 4355
200 CMD_ADD
 city_id:   6  city_id:  39  limit: 22757
200 CMD_ADD
 city_id:  18  city_id:  11  limit: 23249
200 CMD_ADD
 city_id:  22  city_id:  15  limit: 12717
200 CMD_ADD
 city_id:  24  city_id:   9  limit: 7079
200 CMD_ADD
 city_id:  10  city_id:  11  limit: 25985
200 CMD_ADD
 city_id:  12  city_id:   5  limit: 1403
300 CMD_CALC
 sender_city_id:  24  receiver_city_id:   9  number_of_stopover: 2
 stopover_city_id: 15
 stopover_city_id: 28
 answer: 12717
200 CMD_ADD
 city_id:  26  city_id:  11  limit: 27713
200 CMD_ADD
 city_id:  32  city_id:  25  limit: 7367
200 CMD_ADD
 city_id:  12  city_id:  21  limit: 14467
200 CMD_ADD
 city_id:  16  city_id:  33  limit: 15039
300 CMD_CALC
 sender_city_id:  20  receiver_city_id:  21  number_of_stopover: 1
 stopover_city_id: 27
 answer: 11608
200 CMD_ADD
 city_id:   7  city_id:  28  limit: 3342
300 CMD_CALC
 sender_city_id:  11  receiver_city_id:  32  number_of_stopover: 3
 stopover_city_id: 30
 stopover_city_id: 39
 stopover_city_id: 12
 answer: 16176
200 CMD_ADD
 city_id:   2  city_id:  35  limit: 17369
200 CMD_ADD
 city_id:  22  city_id:   7  limit: 15669
200 CMD_ADD
 city_id:   2  city_id:  11  limit: 28417
200 CMD_ADD
 city_id:   6  city_id:  31  limit: 14381
200 CMD_ADD
 city_id:   2  city_id:  19  limit: 22265
200 CMD_ADD
 city_id:  20  city_id:  13  limit: 10915
200 CMD_ADD
 city_id:  24  city_id:   1  limit: 24991
200 CMD_ADD
 city_id:  12  city_id:  29  limit: 2427
200 CMD_ADD
 city_id:   8  city_id:   9  limit: 21943
200 CMD_ADD
 city_id:  36  city_id:  21  limit: 18115
200 CMD_ADD
 city_id:   2  city_id:  27  limit: 25641
200 CMD_ADD
 city_id:  38  city_id:   7  limit: 23965
200 CMD_ADD
 city_id:  26  city_id:   3  limit: 12169
200 CMD_ADD
 city_id:  14  city_id:   7  limit: 6789
200 CMD_ADD
 city_id:   6  city_id:  23  limit: 18725
200 CMD_ADD
 city_id:   8  city_id:  33  limit: 19599
300 CMD_CALC
 sender_city_id:  28  receiver_city_id:  21  number_of_stopover: 3
 stopover_city_id: 11
 stopover_city_id: 24
 stopover_city_id: 9
 answer: 18115
200 CMD_ADD
 city_id:  39  city_id:  36  limit: 29310
200 CMD_ADD
 city_id:  33  city_id:  22  limit: 29584
200 CMD_ADD
 city_id:   5  city_id:  18  limit: 828
200 CMD_ADD
 city_id:  13  city_id:  10  limit: 3668
200 CMD_ADD
 city_id:  25  city_id:  30  limit: 11728
200 CMD_ADD
 city_id:  19  city_id:  32  limit: 24770
200 CMD_ADD
 city_id:  31  city_id:  20  limit: 13294
200 CMD_ADD
 city_id:  35  city_id:  16  limit: 8698
300 CMD_CALC
 sender_city_id:  15  receiver_city_id:  28  number_of_stopover: 2
 stopover_city_id: 10
 stopover_city_id: 11
 answer: 16880
200 CMD_ADD
 city_id:  33  city_id:  14  limit: 9032
200 CMD_ADD
 city_id:  13  city_id:   2  limit: 17844
200 CMD_ADD
 city_id:  29  city_id:  26  limit: 27660
200 CMD_ADD
 city_id:   9  city_id:   6  limit: 3928
200 CMD_ADD
 city_id:  37  city_id:  34  limit: 7796
200 CMD_ADD
 city_id:  17  city_id:  14  limit: 14176
200 CMD_ADD
 city_id:  21  city_id:  18  limit: 4876
200 CMD_ADD
 city_id:  37  city_id:   2  limit: 2964
200 CMD_ADD
 city_id:  33  city_id:   6  limit: 16976
200 CMD_ADD
 city_id:  21  city_id:  10  limit: 25468
200 CMD_ADD
 city_id:  31  city_id:  12  limit: 13054
200 CMD_ADD
 city_id:  19  city_id:   8  limit: 8314
200 CMD_ADD
 city_id:  23  city_id:  28  limit: 4502
300 CMD_CALC
 sender_city_id:  27  receiver_city_id:  16  number_of_stopover: 2
 stopover_city_id: 6
 stopover_city_id: 31
 answer: 19058
200 CMD_ADD
 city_id:   5  city_id:   2  limit: 25876
200 CMD_ADD
 city_id:   1  city_id:   6  limit: 14720
200 CMD_ADD
 city_id:   5  city_id:  10  limit: 23100
200 CMD_ADD
 city_id:  17  city_id:  22  limit: 10712
200 CMD_ADD
 city_id:  21  city_id:  34  limit: 10836
200 CMD_ADD
 city_id:  17  city_id:  30  limit: 13152
200 CMD_ADD
 city_id:  29  city_id:  34  limit: 3612
200 CMD_ADD
 city_id:   1  city_id:  30  limit: 7816
200 CMD_ADD
 city_id:  29  city_id:   2  limit: 14532
300 CMD_CALC
 sender_city_id:  25  receiver_city_id:  38  number_of_stopover: 3
 stopover_city_id: 20
 stopover_city_id: 29
 stopover_city_id: 34
 answer: 18099
200 CMD_ADD
 city_id:  18  city_id:  19  limit: 15217
200 CMD_ADD
 city_id:  30  city_id:  39  limit: 16413
200 CMD_ADD
 city_id:  26  city_id:  35  limit: 21593
200 CMD_ADD
 city_id:  12  city_id:  13  limit: 14931
200 CMD_ADD
 city_id:  38  city_id:  39  limit: 29069
200 CMD_ADD
 city_id:  24  city_id:  17  limit: 19271
200 CMD_ADD
 city_id:   2  city_id:   3  limit: 17249
200 CMD_ADD
 city_id:   4  city_id:  29  limit: 123
300 CMD_CALC
 sender_city_id:   0  receiver_city_id:  33  number_of_stopover: 1
 stopover_city_id: 15
 answer: 13986
200 CMD_ADD
 city_id:  27  city_id:   8  limit: 22826
200 CMD_ADD
 city_id:   1  city_id:  38  limit: 18184
200 CMD_ADD
 city_id:  11  city_id:  16  limit: 16618
200 CMD_ADD
 city_id:  23  city_id:   4  limit: 14230
200 CMD_ADD
 city_id:  11  city_id:   0  limit: 4810
200 CMD_ADD
 city_id:  21  city_id:   2  limit: 18972
200 CMD_ADD
 city_id:   1  city_id:  22  limit: 14984
200 CMD_ADD
 city_id:  37  city_id:  18  limit: 19708
200 CMD_ADD
 city_id:   9  city_id:  38  limit: 3416
200 CMD_ADD
 city_id:  19  city_id:  16  limit: 13354
200 CMD_ADD
 city_id:  15  city_id:  28  limit: 26038
300 CMD_CALC
 sender_city_id:  11  receiver_city_id:   8  number_of_stopover: 1
 stopover_city_id: 14
 answer: 18624
200
100 CMD_INIT
 number_of_city: 50  number_of_road: 60
 city_id:   1  city_id:  25  limit: 28404
 city_id:  11  city_id:  43  limit: 10497
 city_id:  19  city_id:  20  limit: 22538
 city_id:  13  city_id:   9  li
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
import heapq
from collections import defaultdict
def init(N, K, sCity, eCity, mLimit):
	global INF, weights, graph, g_N, path_memo
	path_memo = defaultdict(list)

	INF = 10 ** 18
	g_N = N

	graph = [ [] for _ in range(N)]


	weights = [[0] * N for _ in range(N)]
	for k in range(K):
		weights[sCity[k]][eCity[k]] = mLimit[k]
		weights[eCity[k]][sCity[k]] = mLimit[k]
		graph[sCity[k]].append(eCity[k])
		graph[eCity[k]].append(sCity[k])

	return


def add(sCity, eCity, mLimit):
	global path_memo
	path_memo = defaultdict(list)
	weights[sCity][eCity] = mLimit
	weights[eCity][sCity] = mLimit
	graph[sCity].append(eCity)
	graph[eCity].append(sCity)
	return

def dijkstra(start):
	dist = [-1] * g_N
	hq = []
	dist[start] = INF
	heapq.heappush(hq, [-INF, start])

	while hq:
		neg_weight, cur_node = heapq.heappop(hq)
		cur_weight = -neg_weight

		if dist[cur_node] > cur_weight:
			continue

		for nxt_node in graph[cur_node]:

			cur_limit = weights[cur_node][nxt_node]
			move_weight = min(cur_weight, cur_limit)

			if dist[nxt_node] >= move_weight:
				continue

			dist[nxt_node] = move_weight
			heapq.heappush(hq, [-move_weight, nxt_node])

	return dist

def calculate(sCity, eCity, M, mStopover):

	# print("debug dijk", dijkstra(sCity))
	answer = INF

	ret = dijkstra(sCity)


	for i in mStopover:
		if ret[i] == -1:
			return -1
		else:
			answer = min(answer, ret[i])
	if ret[eCity] == -1:
		return -1

	answer = min(answer, ret[eCity])
	return answer


# ── Main (수정 불가) ──
import sys
# (합쳐서 실행하므로 import 제거)

CMD_INIT = 100
CMD_ADD = 200
CMD_CALC = 300

def run():
	q = int(sys.stdin.readline())
	okay = False

	sCityArr = []
	eCityArr = []
	mLimitArr = []

	for i in range(q):
		cmd = int(sys.stdin.readline().split()[0])

		if cmd == CMD_INIT:
			inputarray = sys.stdin.readline().split()
			n = int(inputarray[1])
			k = int(inputarray[3])
			for _ in range(k):
				road = sys.stdin.readline().split()
				sCityArr.append(int(road[1]))
				eCityArr.append(int(road[3]))
				mLimitArr.append(int(road[5]))

			init(n, k, sCityArr, eCityArr, mLimitArr)
			okay = True
		elif cmd == CMD_ADD:
			inputarray = sys.stdin.readline().split()
			sCity = int(inputarray[1])
			eCity = int(inputarray[3])
			mLimit = int(inputarray[5])
			add(sCity, eCity, mLimit)
		elif cmd == CMD_CALC:
			inputarray = sys.stdin.readline().split()
			sCity = int(inputarray[1])
			eCity = int(inputarray[3])
			m = int(inputarray[5])
			mStopover = []
			for _ in range(m):
				mStopover.append(int(sys.stdin.readline().split()[1]))

			ans = int(sys.stdin.readline().split()[1])
			ret = calculate(sCity, eCity, m, mStopover)
			if ans != ret:
				okay = False
		else:
			okay = False

	return okay


if __name__ == '__main__':
	#sys.stdin = open('sample_input.txt', 'r')
	inputarray = sys.stdin.readline().split()
	TC = int(inputarray[0])
	MARK = int(inputarray[1])

	for testcase in range(1, TC + 1):
		score = MARK if run() else 0
		print("#%d %d" % (testcase, score), flush = True)
