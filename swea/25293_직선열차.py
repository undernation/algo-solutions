"""
SWEA 25293  직선열차
https://swexpertacademy.com/main/talk/solvingClub/problemView.do?solveclubId=AZt8IiBqxEDHBIN6&contestProbId=AZjgXBL6ScPHBITM&probBoxId=AZt8IiBqxEHHBIN6&type=PROBLEM

풀이일 : 2026-09-02   결과: 품
한도   : time 25개 테스트케이스를 합쳐서 C++의 경우 3초 / Java의 경우 3초 / Python의 경우 5초 / memory 힙, 정적 메모리 합쳐서 262144 kbytes 이내, 스택 메모리 1024 kbytes 이내 / time_sec 5
난이도 : D6  |  정답률 69.74%
제약   : 1. 각 테스트 케이스 시작 시 init() 함수가 호출된다.
제약   : 2. 각 테스트 케이스에서 add() 함수의 호출 횟수는 150 이하이다.
제약   : 3. 각 테스트 케이스에서 remove() 함수의 호출 횟수는 100 이하이다.
제약   : 4. 각 테스트 케이스에서 calculate() 함수의 호출 횟수는 50 이하이다.

[채점] accepted  1/1  (6.513s)

[문제]
N개의 열차 역이 직선으로 주어진다. 각 역은 1부터 N까지 ID값을 가진다.

직선으로 왕복 운행하는 열차가 추가될 때, 시작역과 종착역, 그리고 정차 역의 간격이 주어진다.

출발 역에서 도착 역으로 가는데 필요한 최소 환승 횟수를 구하고자 한다.

[Fig. 1]은 20개의 열차 역이 주어진 예이다.

700 열차의 시작역은 2번 역이고 종착역은 16번 역이다. 정차 역의 간격은 7이다.

100 열차의 시작역은 9번 역이고 종착역은 18번 역이다. 정차 역의 간격은 3이다.

300 열차의 시작역은 1번 역이고 종착역은 16번 역이다. 정차 역의 간격은 5이다.

200 열차의 시작역은 4번 역이고 종착역은 18번 역이다. 정차 역의 간격은 7이다.

[[IMG:1]]

[Fig. 1]

15번 역에서 16번 역으로 가는 경로를 살펴보자.

15번 역에서 100 열차를 타고 18번 역으로 이동한 다음에, 200 열차를 타고 11번 역으로 이동한다.

11번 역에서 300 열차를 타고 16번 역으로 이동한다. 총 2번의 환승을 했다.

다른 방법으로, 15번 역에서 100 열차를 타고 9번 역으로 이동한 다음에, 700 열차를 타고 16번 역으로 이동한다.

총 1번의 환승을 했다. 이 방법이 최소 환승 횟수로 이동하는 경로이다.

아래 API 설명을 참조하여 각 함수를 구현하라.

※ 아래 함수 signature는 C/C++에 대한 것으로 다른 언어에 대해서는 제공되는 Main과 User Code를 참고하라.

아래는 User Code 부분에 작성해야 하는 API 의 설명이다.

void init(int N, int K, int mId[], int sId[], int eId[], int mInterval[])

각 테스트 케이스의 처음에 호출된다.

N개의 열차 역이 주어진다. 각 역은 1부터 N까지 ID값을 가진다.

K개의 왕복 운행하는 열차 정보가 주어진다. 각 열차의 ID, 시작역과 종착역, 그리고 정차 역의 간격이 주어진다.

종착역은, 항상 시작역에 정차 간격의 배수를 더한 값이다.

시작역과 종착역이 동일한 경우는 없다.

열차 ID가 서로 같은 경우는 없다.

Parameters

N: 열차 역의 개수 ( 20 ≤ N ≤ 100,000 )

K: 열차의 개수 ( 3 ≤ K ≤ 50 )

(0 ≤ i ＜ K)인 모든 i에 대해,

mId[i]: 열차 i의 ID ( 1 ≤ mId[i] ≤ 1,000,000,000 )

sId[i]: 열차 i의 시작역 ( 1 ≤ sId[i] ≤ N - 3 )

eId[i]: 열차 i의 종착역 ( sId[i] < eId[i] ≤ N )

mInterval[i]: 정차 역의 간격 ( 3 ≤ mInterval[i] ≤ 50 )

void add(int mId, int sId, int eId, int mInterval)

시작역이 sId, 종착역이 eId이고, 정차 역의 간격이 mInterval인 mId 열차를 추가한다.

해당 열차는 시작역과 종착역을 왕복 운행한다.

종착역은, 항상 시작역에 정차 간격의 배수를 더한 값이다.

시작역과 종착역이 동일한 경우는 없다.

init()에 없던 새로운 열차 역은 주어지지 않는다.

mId 값으로 이미 존재하는 열차의 ID가 주어지는 경우는 없다.

Parameters

mId: 열차의 ID ( 1 ≤ mId ≤ 1,000,000,000 )

sId: 열차의 시작역 ( 1 ≤ sId ≤ N - 3 )

eId: 열차의 종착역 ( sId < eId ≤ N )

mInterval: 정차 역의 간격 ( 3 ≤ mInterval ≤ 50 )

void remove(int mId)

mId 열차를 제거한다.

존재하지 않는 열차의 ID가 주어지는 경우는 없다.

Parameters

mId: 열차의 ID ( 1 ≤ mId ≤ 1,000,000,000 )

int calculate(int sId, int eId)

sId 역에서 eId 역으로 가는데 필요한 최소 환승 횟수를 반환한다.

환승 없이 갈 수 있다면, 최소 환승 횟수는 0이 된다.

sId 역에서 eId 역으로 이동할 수 있는 방법이 없다면, -1을 반환한다.

sId와 eId가 서로 같은 경우는 없다.

Parameters

sId: 출발 역 ( 1 ≤ sId ≤ N )

eId: 도착 역 ( 1 ≤ eId ≤ N )

Returns

sId 역에서 eId 역으로 이동이 가능하다면, 최소 환승 횟수를 반환한다.

불가능하다면, -1을 반환한다.

[예제 1]
입력:
25 100
7
100 CMD_INIT
 number_of_station: 20  number_of_train: 3
 train_id:       200  departure_station_id:     4  arrival_station_id:    18  interval: 7
 train_id:       300  departure_station_id:     1  arrival_station_id:    16  interval: 5
 train_id:       100  departure_station_id:     9  arrival_station_id:    18  interval: 3
400 CMD_CALC
 departure_station_id:    15  arrival_station_id:    16
 answer: 2
200 CMD_ADD
 train_id:       700  departure_station_id:     2  arrival_station_id:    16  interval: 7
300 CMD_REMOVE
 train_id:       300
400 CMD_CALC
 departure_station_id:     4  arrival_station_id:    20
 answer: -1
200 CMD_ADD
 train_id:       500  departure_station_id:    16  arrival_station_id:    20  interval: 4
400 CMD_CALC
 departure_station_id:     4  arrival_station_id:    20
 answer: 3
20
100 CMD_INIT
 number_of_station: 1000  number_of_train: 30
 train_id: 350928278  departure_station_id:   809  arrival_station_id:   851  interval: 14
 train_id: 629579282  departure_station_id:   779  arrival_station_id:   809  interval: 10
 train_id: 794471794  departure_station_id:   221  arrival_station_id:   273  interval: 26
 train_id: 235296706  departure_station_id:   583  arrival_station_id:   613  interval: 10
 train_id: 725935358  departure_station_id:   593  arrival_station_id:   615  interval: 22
 train_id: 538766930  departure_station_id:   459  arrival_station_id:   501  interval: 42
 train_id:  84176862  departure_station_id:   813  arrival_station_id:   851  interval: 38
 train_id: 952263386  departure_station_id:   851  arrival_station_id:   901  interval: 50
 train_id:  88489754  departure_station_id:   395  arrival_station_id:   445  interval: 50
 train_id: 106424790  departure_station_id:   445  arrival_station_id:   473  interval: 14
 train_id: 214614198  departure_station_id:   633  arrival_station_id:   679  interval: 46
 train_id:     12346  departure_station_id:     7  arrival_station_id:   257  interval: 50
 train_id: 179132042  departure_station_id:   523  arrival_station_id:   541  interval: 18
 train_id: 229283574  departure_station_id:   207  arrival_station_id:   235  interval: 14
 train_id: 787378758  departure_station_id:   541  arrival_station_id:   583  interval: 14
 train_id: 588911646  departure_station_id:   373  arrival_station_id:   395  interval: 22
 train_id: 929199098  departure_station_id:   615  arrival_station_id:   651  interval: 18
 train_id: 121308586  departure_station_id:   269  arrival_station_id:   319  interval: 50
 train_id: 263435058  departure_station_id:   679  arrival_station_id:   739  interval: 10
 train_id: 214206318  departure_station_id:   689  arrival_station_id:   733  interval: 22
 train_id:  65456802  departure_station_id:   787  arrival_station_id:   813  interval: 26
 train_id: 393101606  departure_station_id:   745  arrival_station_id:   801  interval: 14
 train_id: 103497954  departure_station_id:   347  arrival_station_id:   399  interval: 26
 train_id: 522586702  departure_station_id:   735  arrival_station_id:   779  interval: 22
 train_id: 370913198  departure_station_id:   247  arrival_station_id:   291  interval: 22
 train_id: 343235942  departure_station_id:   319  arrival_station_id:   361  interval: 14
 train_id: 450231882  departure_station_id:   701  arrival_station_id:   735  interval: 34
 train_id: 749508458  departure_station_id:   711  arrival_station_id:   745  interval: 34
 train_id: 460797446  departure_station_id:   659  arrival_station_id:   701  interval: 14
 train_id: 837716110  departure_station_id:   501  arrival_station_id:   523  interval: 22
400 CMD_CALC
 departure_station_id:     7  arrival_station_id:   901
 answer: 24
300 CMD_REMOVE
 train_id: 229283574
300 CMD_REMOVE
 train_id: 538766930
300 CMD_REMOVE
 train_id: 214614198
300 CMD_REMOVE
 train_id:  84176862
400 CMD_CALC
 departure_station_id:    51  arrival_station_id:   400
 answer: -1
200 CMD_ADD
 train_id: 700328857  departure_station_id:   160  arrival_station_id:   416  interval: 32
300 CMD_REMOVE
 train_id: 370913198
200 CMD_ADD
 train_id:  17565615  departure_station_id:   327  arrival_station_id:   730  interval: 31
300 CMD_REMOVE
 train_id: 106424790
200 CMD_ADD
 train_id: 920259938  departure_station_id:   271  arrival_station_id:   567  interval: 37
200 CMD_ADD
 train_id: 864555418  departure_station_id:   103  arrival_station_id:   259  interval: 39
300 CMD_REMOVE
 train_id: 837716110
300 CMD_REMOVE
 train_id: 629579282
400 CMD_CALC
 departure_station_id:   207  arrival_station_id:   252
 answer: -1
200 CMD_ADD
 train_id: 115638805  departure_station_id:     5  arrival_station_id:    95  interval: 5
200 CMD_ADD
 train_id: 782989754  departure_station_id:   338  arrival_station_id:   734  interval: 18
200 CMD_ADD
 train_id: 192992779  departure_station_id:    12  arrival_station_id:    82  interval: 14
400 CMD_CALC
 departure_station_id:   572  arrival_station_id:   813
 answer: 6
30
100 CMD_INIT
 number_of_station: 2000  number_of_train: 30
 train_id: 881654895  departure_station_id:  1722  arrival_station_id:  1827  interval: 15
 train_id:  55989559  departure_station_id:  1112  arrival_station_id:  1224  interval: 7
 train_id: 326098459  departure_station_id:  1306  arrival_station_id:  1392  interval: 43
 train_id:  94309495  departure_station_id:   124  arrival_station_id:   239  interval: 23
 train_id:  45902415  departure_station_id:   300  arrival_station_id:   424  interval: 31
 train_id:  67689887  departure_station_id:    10  arrival_station_id:    70  interval: 15
 train_id: 428924179  departure_station_id:   896  arrival_station_id:   966  interval: 35
 train_id: 208253115  departure_station_id:   828  arrival_station_id:   894  interval: 11
 train_id: 104955687  departure_station_id:   451  arrival_station_id:   528  interval: 7
 train_id: 755265803  departure_station_id:   617  arrival_station_id:   703  interval: 43
 train_id: 468154883  departure_station_id:   216  arrival_station_id:   300  interval: 3
 train_id:  10338791  departure_station_id:  1392  arrival_station_id:  1483  interval: 7
 train_id: 607495831  departure_station_id:  1587  arrival_station_id:  1665  interval: 39
 train_id: 656362751  departure_station_id:   557  arrival_station_id:   662  interval: 15
 train_id: 719923135  departure_station_id:  1464  arrival_station_id:  1539  interval: 15
 train_id: 230057907  departure_station_id:   458  arrival_station_id:   557  interval: 3
 train_id: 285104223  departure_station_id:   966  arrival_station_id:  1086  interval: 15
 train_id: 382797419  departure_station_id:  1026  arrival_station_id:  1112  interval: 43
 train_id: 303996843  departure_station_id:    70  arrival_station_id:   124  interval: 27
 train_id:  57939571  departure_station_id:  1413  arrival_station_id:  1536  interval: 3
 train_id: 938846075  departure_station_id:  1782  arrival_station_id:  1836  interval: 27
 train_id: 304609475  departure_station_id:  1140  arrival_station_id:  1212  interval: 3
 train_id: 580659119  departure_station_id:   797  arrival_station_id:   890  interval: 31
 train_id: 602900615  departure_station_id:   850  arrival_station_id:   919  interval: 23
 train_id: 971191255  departure_station_id:   703  arrival_station_id:   787  interval: 7
 train_id: 829503435  departure_station_id:  1479  arrival_station_id:  1587  interval: 27
 train_id: 196354403  departure_station_id:   759  arrival_station_id:   873  interval: 19
 train_id: 849018915  departure_station_id:  1665  arrival_station_id:  1760  interval: 19
 train_id:  62960475  departure_station_id:   424  arrival_station_id:   505  interval: 27
 train_id: 268492559  departure_station_id:  1212  arrival_station_id:  1306  interval: 47
400 CMD_CALC
 departure_station_id:   617  arrival_station_id:   270
 answer: 5
300 CMD_REMOVE
 train_id: 104955687
200 CMD_ADD
 train_id: 446154783  departure_station_id:   565  arrival_station_id:  1290  interval: 25
300 CMD_REMOVE
 train_id: 468154883
200 CMD_ADD
 train_id: 864079252  departure_station_id:   518  arrival_station_id:  1190  interval: 14
300 CMD_REMOVE
 train_id: 446154783
300 CMD_REMOVE
 train_id: 382797419
200 CMD_ADD
 train_id: 625459251  departure_station_id:   158  arrival_station_id:   408  interval: 50
300 CMD_REMOVE
 train_id: 656362751
400 CMD_CALC
 departure_station_id:  1144  arrival_station_id:  1889
 answer: -1
300 CMD_REMOVE
 train_id: 285104223
300 CMD_REMOVE
 train_id: 196354403
300 CMD_REMOVE
 train_id: 971191255
300 CMD_REMOVE
 train_id: 602900615
200 CMD_ADD
 train_id: 352758050  departure_station_id:   637  arrival_station_id:  1451  interval: 37
200 CMD_ADD
 train_id:  13261658  departure_station_id:   494  arrival_station_id:  1088  interval: 18
200 CMD_ADD
 train_id: 301046059  departure_station_id:   375  arrival_station_id:   870  interval: 11
200 CMD_ADD
 train_id: 869350904  departure_station_id:   463  arrival_station_id:  1109  interval: 19
200 CMD_ADD
 train_id: 580596976  departure_station_id:   828  arrival_station_id:  1748  interval: 40
300 CMD_REMOVE
 train_id:  94309495
400 CMD_CALC
 departure_station_id:  1028  arrival_station_id:   461
 answer: 2
200 CMD_ADD
 train_id: 924541728  departure_station_id:    48  arrival_station_id:   288  interval: 40
400 CMD_CALC
 departure_station_id:  1112  arrival_station_id:   545
 answer: 3
200 CMD_ADD
 train_id: 218601002  departure_station_id:   502  arrival_station_id:  1114  interval: 34
300 CMD_REMOVE
 train_id: 230057907
300 CMD_REMOVE
 train_id: 938846075
300 CMD_REMOVE
 train_id:  13261658
200 CMD_ADD
 train_id: 282443125  departure_station_id:   817  arrival_station_id:  1742  interval: 37
400 CMD_CALC
 departure_station_id:  1437  arrival_station_id:  1170
 answer: 2
40
100 CMD_INIT
 number_of_station: 4000  number_of_train: 40
 train_id:  93541094  departure_station_id:  1017  arrival_station_id:  1167  interval: 30
 train_id: 427394062  departure_station_id:  1839  arrival_station_id:  1991  interval: 38
 train_id: 598928458  departure_station_id:   225  arrival_station_id:   375  interval: 50
 train_id: 913137094  departure_station_id:  2123  arrival_station_id:  2319  interval: 14
 train_id: 901262326  departure_station_id:  3171  arrival_station_id:  3401  interval: 46
 train_id: 352450974  departure_station_id:  1347  arrival_station_id:  1479  interval: 6
 train_id: 308281434  departure_station_id:  3331  arrival_station_id:  3493  interval: 18
 train_id: 122572406  departure_station_id:   529  arrival_station_id:   753  interval: 14
 train_id: 831365510  departure_station_id:  3575  arrival_station_id:  3813  interval: 14
 train_id: 131630542  departure_station_id:  3773  arrival_station_id:  3925  interval: 38
 train_id: 622150442  departure_station_id:   867  arrival_station_id:  1067  interval: 50
 train_id: 432598182  departure_station_id:  3033  arrival_station_id:  3201  interval: 14
 train_id: 737207682  departure_station_id:   305  arrival_station_id:   455  interval: 10
 train_id: 118603786  departure_station_id:  1953  arrival_station_id:  2157  interval: 34
 train_id: 418402682  departure_station_id:  2403  arrival_station_id:  2583  interval: 18
 train_id: 862748438  departure_station_id:  3493  arrival_station_id:  3619  interval: 14
 train_id:  60974834  departure_station_id:   627  arrival_station_id:   795  interval: 42
 train_id: 101290650  departure_station_id:  1413  arrival_station_id:  1563  interval: 50
 train_id: 129965514  departure_station_id:  3669  arrival_station_id:  3849  interval: 18
 train_id: 262168978  departure_station_id:  3605  arrival_station_id:  3815  interval: 42
 train_id: 155745090  departure_station_id:  2249  arrival_station_id:  2457  interval: 26
 train_id: 987794046  departure_station_id:  2327  arrival_station_id:  2441  interval: 38
 train_id: 160472890  departure_station_id:  3257  arrival_station_id:  3437  interval: 18
 train_id: 581646434  departure_station_id:  1137  arrival_station_id:  1347  interval: 42
 train_id: 126203570  departure_station_id:  2607  arrival_station_id:  2815  interval: 26
 train_id: 409135918  departure_station_id:   753  arrival_station_id:   905  interval: 38
 train_id: 306534590  departure_station_id:   385  arrival_station_id:   517  interval: 22
 train_id: 721718290  departure_station_id:     9  arrival_station_id:   303  interval: 42
 train_id: 393283330  departure_station_id:  3547  arrival_station_id:  3757  interval: 42
 train_id: 357272298  departure_station_id:  2883  arrival_station_id:  3033  interval: 50
 train_id:  34475246  departure_station_id:  2685  arrival_station_id:  2905  interval: 22
 train_id: 738242082  departure_station_id:  3187  arrival_station_id:  3317  interval: 26
 train_id: 538420230  departure_station_id:   275  arrival_station_id:   455  interval: 30
 train_id:  47774138  departure_station_id:   495  arrival_station_id:   665  interval: 34
 train_id: 182680638  departure_station_id:  3361  arrival_station_id:  3589  interval: 38
 train_id: 807533522  departure_station_id:  1605  arrival_station_id:  1839  interval: 26
 train_id: 710393686  departure_station_id:  1513  arrival_station_id:  1651  interval: 46
 train_id: 536756574  departure_station_id:  3265  arrival_station_id:  3419  interval: 22
 train_id:  85082702  departure_station_id:   135  arrival_station_id:   327  interval: 6
 train_id: 496733238  departure_station_id:  2457  arrival_station_id:  2607  interval: 30
400 CMD_CALC
 departure_station_id:     9  arrival_station_id:  3925
 answer: 28
300 CMD_REMOVE
 train_id: 862748438
300 CMD_REMOVE
 train_id: 536756574
200 CMD_ADD
 train_id: 277329700  departure_station_id:  1571  arrival_station_id:  3528  interval: 19
300 CMD_REMOVE
 train_id: 721718290
200 CMD_ADD
 train_id: 126683910  departure_station_id:    25  arrival_station_id:   331  interval: 9
200 CMD_ADD
 train_id: 404791230  departure_station_id:   697  arrival_station_id:  1615  interval: 17
200 CMD_ADD
 train_id: 228657526  departure_station_id:   185  arrival_station_id:   635  interval: 25
300 CMD_REMOVE
 train_id: 427394062
300 CMD_REMOVE
 train_id: 901262326
200 CMD_ADD
 train_id:  26510378  departure_station_id:  1734  arrival_station_id:  3706  interval: 34
300 CMD_REMOVE
 train_id:  93541094
300 CMD_REMOVE
 train_id: 737207682
200 CMD_ADD
 train_id: 856883335  departure_station_id:  1543  arrival_station_id:  3349  interval: 7
400 CMD_CALC
 departure_station_id:   261  arrival_station_id:  3258
 answer: 4
300 CMD_REMOVE
 train_id: 155745090
400 CMD_CALC
 departure_station_id:  1122  arrival_station_id:   563
 answer: 2
200 CMD_ADD
 train_id: 850555824  departure_station_id:  1284  arrival_station_id:  2772  interval: 24
300 CMD_REMOVE
 train_id: 913137094
300 CMD_REMOVE
 train_id: 856883335
200 CMD_ADD
 train_id: 305088085  departure_station_id:  1101  arrival_station_id:  2531  interval: 5
300 CMD_REMOVE
 train_id: 308281434
300 CMD_REMOVE
 train_id: 228657526
200 CMD_ADD
 train_id: 469738422  departure_station_id:   310  arrival_station_id:   820  interval: 34
200 CMD_ADD
 train_id:  57496059  departure_station_id:    59  arrival_station_id:   444  interval: 11
200 CMD_ADD
 train_id: 890685320  departure_station_id:   126  arrival_station_id:   526  interval: 50
200 CMD_ADD
 train_id:   6939563  departure_station_id:   870  arrival_station_id:  2130  interval: 42
200 CMD_ADD
 train_id: 705726467  departure_station_id:   798  arrival_station_id:  1848  interval: 50
200 CMD_ADD
 train_id: 240983899  departure_station_id:   990  arrival_station_id:  2180  interval: 10
200 CMD_ADD
 train_id: 471875507  departure_station_id:   395  arrival_station_id:  1022  interval: 19
300 CMD_REMOVE
 train_id: 890685320
300 CMD_REMOVE
 train_id: 160472890
200 CMD_ADD
 train_id: 579688316  departure_station_id:   391  arrival_station_id:   966  interval: 23
400 CMD_CALC
 departure_station_id:  2905  arrival_station_id:  2110
 answer: 3
200 CMD_ADD
 train_id: 304184585  departure_station_id:  1214  arrival_station_id:  2710  interval: 34
200 CMD_ADD
 train_id: 279286443  departure_station_id:  1365  arrival_station_id:  3003  interval: 21
200 CMD_ADD
 train_id: 864995402  departure_station_id:   957  arrival_station_id:  2262  interval: 45
300 CMD_REMOVE
 train_id:  34475246
400 CMD_CALC
 departure_station_id:  1901  arrival_station_id:   322
 answer: 4
80
100 CMD_INIT
 number_of_station: 8000  number_of_train: 40
 train_id: 384472608  departure_station_id:  5595  arrival_station_id:  5987  interval: 8
 train_id: 709659516  departure_station_id:  3315  arrival_station_id:  3575  interval: 20
 train_id: 796616856  departure_station_id:   239  arrival_station_id:   543  interval: 16
 train_id: 223081056  departure_station_id:  3275  arrival_station_id:  3675  interval: 40
 train_id:  19884324  departure_station_id:  1471  arrival_station_id:  1927  interval: 12
 train_id: 138960920  departure_station_id:  5759  arrival_station_id:  6143  interval: 48
 train_id: 867753768  departure_station_id:  5351  arrival_station_id:  5703  interval: 16
 train_id: 912711056  departure_station_id:   871  arrival_station_id:  1207  interval: 24
 train_id: 759924404  departure_station_id:  5807  arrival_station_id:  6115  interval: 28
 train_id: 356001160  departure_station_id:  1135  arrival_station_id:  1471  interval: 48
 train_id: 712034424  departure_station_id:  1967  arrival_station_id:  2303  interval: 48
 train_id: 844754132  departure_station_id:  4923  arrival_station_id:  5415  interval: 12
 train_id: 275219824  departure_station_id:  2555  arrival_station_id:  3011  interval: 8
 train_id: 519345004  departure_station_id:  3771  arrival_station_id:  4211  interval: 20
 train_id: 971662172  departure_station_id:  4131  arrival_station_id:  4559  interval: 4
 train_id: 959243972  departure_station_id:  5399  arrival_station_id:  5679  interval: 28
 train_id: 881109780  departure_station_id:  2207  arrival_station_id:  2591  interval: 12
 train_id: 675740488  departure_station_id:  3991  arrival_station_id:  4471  interval: 32
 train_id: 520509740  departure_station_id:  6207  arrival_station_id:  6627  interval: 20
 train_id: 125919540  departure_station_id:   479  arrival_station_id:   899  interval: 28
 train_id: 786523984  departure_station_id:  3587  arrival_station_id:  3987  interval: 8
 train_id: 378434444  departure_station_id:  2787  arrival_station_id:  3259  interval: 4
 train_id: 411879176  departure_station_id:  6427  arrival_station_id:  6859  interval: 48
 train_id: 527303908  departure_station_id:  4055  arrival_station_id:  4559  interval: 12
 train_id: 678562880  departure_station_id:  4091  arrival_station_id:  4411  interval: 40
 train_id: 517664156  departure_station_id:  1859  arrival_station_id:  2363  interval: 36
 train_id: 957075032  departure_station_id:  3335  arrival_station_id:  3623  interval: 48
 train_id: 890703520  departure_station_id:     3  arrival_station_id:   219  interval: 24
 train_id: 575699728  departure_station_id:  6087  arrival_station_id:  6607  interval: 40
 train_id: 791159628  departure_station_id:  5063  arrival_station_id:  5387  interval: 36
 train_id: 994913212  departure_station_id:    99  arrival_station_id:   519  interval: 20
 train_id:  30180144  departure_station_id:  5007  arrival_station_id:  5431  interval: 8
 train_id: 736460416  departure_station_id:  1723  arrival_station_id:  2171  interval: 8
 train_id: 321680700  departure_station_id:  5643  arrival_station_id:  6043  interval: 4
 train_id: 511558572  departure_station_id:   895  arrival_station_id:  1355  interval: 20
 train_id: 865401076  departure_station_id:  3575  arrival_station_id:  3851  interval: 12
 train_id: 881131268  departure_station_id:  3079  arrival_station_id:  3331  interval: 28
 train_id: 608467512  departure_station_id:  4507  arrival_station_id:  4955  interval: 32
 train_id: 886305640  departure_station_id:  3031  arrival_station_id:  3415  interval: 48
 train_id:  57620644  departure_station_id:  6715  arrival_station_id:  7135 
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
from collections import deque, defaultdict


class Train:
    def __init__(self):
        self.start_line = -1
        self.end_line = -1
        self.interval = -1
        self.interval_set = set()
        self.is_ok = False
        self.graph = set()


def init(N, K, mId, sId, eId, mInterval):
    global stations, trains, g_N, memo
    stations = defaultdict(set)
    trains = dict()
    g_N = N
    memo = dict()

    for k in range(K):
        train = Train()
        cur_id = mId[k]
        start = sId[k]
        end = eId[k]
        interval = mInterval[k]

        train.start_line = start
        train.end_line = end
        train.interval = interval
        train.is_ok = True

        # 역별 인터벌 반영.
        while start <= end:
            if stations[start]:
                for another in stations[start]:
                    train.graph.add(another)
                    trains[another].graph.add(cur_id)

            stations[start].add(cur_id)
            train.interval_set.add(start)

            # start 지점에 다른 열차 있으면 그 열차 graph 셋에 저장
            start += interval

        trains[cur_id] = train


# 150
def add(mId, sId, eId, mInterval):
    train = Train()
    cur_id = mId
    start = sId
    end = eId
    interval = mInterval
    memo.clear()

    train.start_line = start
    train.end_line = end
    train.interval = interval
    train.is_ok = True

    # 역별 인터벌 반영.
    while start <= end:
        if stations[start]:
            for another in stations[start]:
                train.graph.add(another)
                trains[another].graph.add(cur_id)

        stations[start].add(cur_id)
        train.interval_set.add(start)
        start += interval

    trains[cur_id] = train


# 100
def remove(mId):
    trains[mId].is_ok = False
    memo.clear()


def check_with_no_transfer(train_id, end_line_id):
    if end_line_id in trains[train_id].interval_set:
        return True
    else:
        return False


def bfs(start_id, end_id):
    start_train_ids = stations[start_id]
    visited = set()

    q = deque()
    # 시간초과 예상지점.
    for start_train_id in start_train_ids:
        if not trains[start_train_id].is_ok:
            continue
        if check_with_no_transfer(start_train_id, end_id):
            memo[(start_id, end_id)] = 0
            return 0
        visited.add(start_train_id)
        # id, cnt
        q.append((start_train_id, 0))

    while q:

        cur_train_id, cur_cnt = q.popleft()
        for nxt_train_id in trains[cur_train_id].graph:
            if not trains[nxt_train_id].is_ok:
                continue
            if nxt_train_id in visited:
                continue
            if check_with_no_transfer(nxt_train_id, end_id):
                memo[(start_id, end_id)] = cur_cnt + 1
                return cur_cnt + 1

            visited.add(nxt_train_id)
            q.append((nxt_train_id, cur_cnt + 1))

    memo[(start_id, end_id)] = -1
    return -1


# 50
def calculate(sId, eId):
    if (sId, eId) in memo:
        return memo[(sId, eId)]
    ret = bfs(sId, eId)
    # print("calculate", ret)
    return ret


# ── Main (수정 불가) ──
import sys
# (합쳐서 실행하므로 import 제거)

CMD_INIT = 100
CMD_ADD = 200
CMD_REMOVE = 300
CMD_CALC = 400

def run():
	q = int(sys.stdin.readline())
	okay = False

	mIdArr = []
	sIdArr = []
	eIdArr = []
	mIntervalArr = []

	for i in range(q):
		inputarray = sys.stdin.readline().split()
		cmd = int(inputarray[0])

		if cmd == CMD_INIT:
			inputarray = sys.stdin.readline().split()
			n = int(inputarray[1])
			k = int(inputarray[3])
			for _ in range(k):
				tinfo = sys.stdin.readline().split()
				mIdArr.append(int(tinfo[1]))
				sIdArr.append(int(tinfo[3]))
				eIdArr.append(int(tinfo[5]))
				mIntervalArr.append(int(tinfo[7]))

			init(n, k, mIdArr, sIdArr, eIdArr, mIntervalArr)
			okay = True
		elif cmd == CMD_ADD:
			inputarray = sys.stdin.readline().split()
			mId = int(inputarray[1])
			sId = int(inputarray[3])
			eId = int(inputarray[5])
			mInterval = int(inputarray[7])
			add(mId, sId, eId, mInterval)
		elif cmd == CMD_REMOVE:
			inputarray = sys.stdin.readline().split()
			mId = int(inputarray[1])
			remove(mId)
		elif cmd == CMD_CALC:
			inputarray = sys.stdin.readline().split()
			sId = int(inputarray[1])
			eId = int(inputarray[3])
			ans = int(sys.stdin.readline().split()[1])
			ret = calculate(sId, eId)
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
