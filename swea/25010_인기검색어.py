"""
SWEA 25010  인기 검색어
https://swexpertacademy.com/main/talk/solvingClub/problemView.do?solveclubId=AZt8IiBqxEDHBIN6&contestProbId=AZih7SL6varHBINp&probBoxId=AZt8IiBqxEHHBIN6&type=PROBLEM

풀이일 : 2026-09-05   결과: 못품
한도   : time 25개 테스트케이스를 합쳐서 C++의 경우 3초 / Java의 경우 3초 / Python의 경우 6초 / memory 힙, 정적 메모리 합쳐서 262144 kbytes 이내, 스택 메모리 1024 kbytes 이내 / time_sec 6
난이도 : D6  |  정답률 76.42%
제약   : 1. 각 테스트 케이스 시작 시 init() 함수가 한 번 호출된다.
제약   : 2. 각 테스트케이스별로 addKeyword() 의 호출횟수는 최대 10,000 회이다.
제약   : 3. 각 테스트케이스별로 top5Keyword() 의 호출횟수는 최대 100 회이다.

[채점] accepted  1/1  (3.219s)

[문제]
실시간으로 Top 5 인기검색어를 찾는 프로그램을 구현해보자.

당신은 사용자들이 입력한 검색어를 순서대로 전달받는다.

그 중 가장 최근에 전달받은 N 개의 검색어를 가지고 Top 5 인기 검색어를 찾아야 한다. (10 ≤ N ≤ 500)

예를 들어, 10,000 개의 검색어가 전달되었고 N = 500 이라면 9,501 ~ 10,000 번째 검색어들로 인기검색어를 찾아야 한다.

N 은 각 테스트케이스의 가장 처음 전달되며, 변하지 않는 값이다.

다음은 유사 검색어에 대한 정의이다.

두 검색어의 길이가 같고 문자가 1 개만 다른 경우, 두 검색어는 유사하다고 한다.

예를 들어, 검색어 “aaaaa” 와 “aaaab” 는 유사하다. “aaaab” 와 “abaab” 도 유사하다

또한 검색어 A와 B가 유사하고, B와 C가 유사할 경우 A와 C도 유사하다. 이 상황에서 새로 전달된 D 와 C가 유사할 경우 A 와 D 도 유사하다.

이런 상황에서 검색어가 더 추가되어 검색어 B 가 최근 N 개의 검색어에 포함되지 않을 경우, A 와 C는 더이상 유사하지 않은 검색어가 될 수도 있음에 유의하라.

다음은 대표 검색어를 선정하는 규칙이다.

당신은 Top5 인기 검색어 list 를 반환할때 유사한 검색어 집합 중에서 대표 검색어를 반환하여야 한다.

한 집합에서 대표 검색어를 선정하는 규칙은 다음과 같다.

최근 N 개의 검색어들 중, 가장 많이 전달된 검색어가 대표 검색어가 된다.

전달된 갯수가 같을 경우, 사전순으로 앞선 검색어가 대표 검색어가 된다.

다음은 인기 검색어를 선정하는 규칙이다.

가장 많이 전달된 검색어 집합의 순위가 높다.

각 집합의 전달된 갯수는 그 집합을 이루고 있는 유사 검색어들의 전달 갯수의 합으로 계산한다.

전달된 갯수가 같을 경우, 대표 검색어 중 사전순으로 앞선 검색어의 순위가 높다.

이러한 규칙으로 우선순위가 높은 5 개의 대표검색어를 찾아야 한다.

아래 API 설명을 참조하여 각 함수를 구현하라.

아래는 User Code 부분에 작성해야 하는 API 의 설명이다.

void init(int N)

테스트 케이스에 대한 초기화 함수.

각 테스트 케이스의 맨 처음 1회 호출된다.

N 은 처리 해야 할 검색어의 갯수를 의미한다.

이 테스트케이스에서는 가장 최근 N 개의 검색어들로 인기 검색어를 찾아야 한다.

초기에는 전달된 검색어가 없는 상태이다.

Parameters

N : 처리해야 할 검색어의 갯수 (10 ≤ N ≤ 500)

void addKeyword(string mKeyword)

새로운 검색어가 추가 된다.

string type 의 경우 C++ 언어에서는 char 배열로 제공된다.

검색어는 길이 3 이상 10 이하이고 영어 소문자로 구성되어 있다.

Parameters

mKeyword : 추가 된 검색어(3 ≤ 검색어의 길이 ≤ 10)

int top5Keyword(string mRet[])

최근 N 개의 검색어 중 가장 우선순위가 높은 인기검색어 5 개를 반환한다.

인기검색어를 선정하는 규칙은 본문을 참고하라.

mRet[] 에는 인기검색어를 순위가 높은 순서대로 저장한다.

이 배열의 0 번째 index 에 가장 순위가 높은 인기검색어를 저장한다.

리턴 값은 mRet 에 저장된 인기 검색어의 갯수이다.

Parameters

mRet : Top 5 인기검색어를 저장할 배열

Return

mRet 에 저장된 인기 검색어 갯수

[예제 1]
입력:
25 100
21
100 10
200 aaa
200 bbb
200 ccc
300 3 aaa bbb ccc
200 bab
300 3 bab aaa ccc
200 bbb
300 3 bbb aaa ccc
200 aab
300 2 bbb ccc
200 aaa
200 bbb
200 ccc
200 aaa
200 aaa
200 aaa
200 aaa
300 2 aaa ccc
200 aaa
300 3 aaa bbb ccc
121
100 20
200 xozsnzth
200 azxwyr
200 wljfp
200 yzxwyr
300 3 azxwyr wljfp xozsnzth
200 werfp
300 4 azxwyr werfp wljfp xozsnzth
200 mdvsc
200 wlrfp
200 zqbuwsuk
200 xecicjezbs
200 lecirjezbs
200 mjdvtq
200 rdvse
200 xecirjeabs
200 rdvwc
200 xecirjezss
200 mjdutq
200 clrfp
200 xomsnzxh
200 iqbmwsuk
200 fzxwyr
200 xecirjeqbs
300 5 clrfp azxwyr mjdutq xecirjeabs iqbmwsuk
200 rdvgc
200 fzxkyr
200 xommnzth
200 iqbuwsik
300 5 clrfp fzxkyr mjdutq rdvgc xecirjeabs
200 iqbuusuk
200 xetirjezbs
200 fzxwcr
200 rgvsc
200 mjdolq
200 xecirnezbs
200 xecirjezbu
200 iqbuwsud
200 xecirdezbs
200 mjnotq
200 tecirjezbs
200 xgcirjezbs
200 iqvuwsuk
200 tomsnzth
200 mjgotq
300 5 mjgotq xecirdezbs fzxkyr fzxwcr iqbuusuk
300 5 mjgotq xecirdezbs fzxkyr fzxwcr iqbuusuk
200 fzxwyd
200 fzxwlr
200 xecircezbs
200 wmrfp
200 xecrrjezbs
200 wlrfm
200 rdvsi
200 rzxwyr
300 5 xecircezbs mjgotq fzxwlr fzxwyd iqbuwsud
200 xexirjezbs
200 iqbuwsuv
200 xecirjeubs
200 ivbuwsuk
200 xomsnzth
200 iqbuwkuk
200 wlrfq
200 tomsnzth
200 fgxwyr
200 rtvsc
200 fzxwyr
200 tomsnzth
300 5 fgxwyr tomsnzth wlrfm iqbuwkuk iqbuwsuv
200 rovsc
200 rpvsc
200 rdvsg
200 mjdktq
200 worfp
300 5 fgxwyr rovsc tomsnzth rdvsg wlrfm
200 xomsnfth
300 5 tomsnzth fgxwyr rovsc rdvsg iqbuwkuk
200 xoxsnzth
200 rdtsc
200 werfp
200 isbuwsuk
200 rwvsc
200 izxwyr
200 xecirjevbs
200 xecirjezbg
200 fzxnyr
200 wdvsc
200 iqbuwsbk
200 ndvsc
200 xomsnztl
200 fztwyr
200 rdhsc
200 nzxwyr
200 jzxwyr
200 rdcsc
200 mddotq
200 rddsc
200 wlqfp
200 fzxwyr
200 iqbewsuk
200 wlrvp
300 5 fztwyr rdcsc ndvsc iqbewsuk iqbuwsbk
300 5 fztwyr rdcsc ndvsc iqbewsuk iqbuwsbk
200 fzxgyr
200 jdvsc
300 5 fztwyr jdvsc rdcsc iqbewsuk iqbuwsbk
200 wlrfp
300 5 fztwyr jdvsc rdcsc wlqfp iqbewsuk
200 xsmsnzth
300 5 fztwyr jdvsc rdcsc wlqfp iqbewsuk
300 5 fztwyr jdvsc rdcsc wlqfp iqbewsuk
200 frxwyr
200 warfp
300 5 frxwyr warfp rdcsc jdvsc iqbewsuk
300 5 frxwyr warfp rdcsc jdvsc iqbewsuk
200 iqbuwsub
300 5 frxwyr warfp rdcsc jdvsc iqbewsuk
200 iqbjwsuk
200 fzxwyy
200 xecirjegbs
300 5 frxwyr warfp rdcsc iqbewsuk iqbuwsub
121
100 20
200 slovgxamwi
200 soovgxvmwi
200 jciedobl
200 jciedpbl
200 fqedxgiac
300 4 jciedobl fqedxgiac slovgxamwi soovgxvmwi
200 lqjdxgiac
200 slovgxvmzi
200 slovgevmwi
300 5 jciedobl fqedxgiac lqjdxgiac slovgevmwi slovgxamwi
200 jhiedzbl
200 skovgxvmwi
200 slovgxvowi
200 lqvdxgiac
200 lqecxgiac
300 5 jciedobl lqjdxgiac skovgxvmwi fqedxgiac jhiedzbl
200 dciedzbl
200 jwiedzbl
200 lqedxiiac
200 jsiedzbl
200 slovgxvlwi
200 lwedxgiac
200 slovguvmwi
200 slovgmvmwi
200 lqedxgiao
200 slovsxvmwi
200 dlovgxvmwi
200 jciedzbz
200 slevgxvmwi
200 jciedzol
200 lqidxgiac
200 slovgxvmwc
200 dciedzbl
200 lqedsgiac
200 jcmedzbl
300 5 dciedzbl jsiedzbl slovgmvmwi dlovgxvmwi jciedzbz
200 llovgxvmwi
200 slovpxvmwi
200 jciedubl
200 lqedxgibc
200 jwiedzbl
300 5 dlovgxvmwi slovgmvmwi slovpxvmwi dciedzbl jciedubl
300 5 dlovgxvmwi slovgmvmwi slovpxvmwi dciedzbl jciedubl
200 jciedznl
200 suovgxvmwi
200 slovgxvmwh
200 glovgxvmwi
200 lqerxgiac
200 lqedxgiac
200 lqedjgiac
200 sqedxgiac
200 jcieszbl
200 slovtxvmwi
200 lqedxgcac
200 jciedzbl
200 jciedznl
200 lqedzgiac
200 fqedxgiac
200 lqedxgial
200 eciedzbl
200 lqedxyiac
200 lqedxgiam
200 jciepzbl
200 lqedxgqac
200 sloegxvmwi
200 lqudxgiac
200 slovgxvmqi
200 lqedrgiac
200 alovgxvmwi
200 slovgyvmwi
200 slovgxomwi
200 lqtdxgiac
300 5 eciedzbl lqedrgiac lqedxgcac lqedxgial lqtdxgiac
300 5 eciedzbl lqedrgiac lqedxgcac lqedxgial lqtdxgiac
200 jciedbbl
300 5 eciedzbl lqedrgiac lqedxgcac lqedxgial lqtdxgiac
300 5 eciedzbl lqedrgiac lqedxgcac lqedxgial lqtdxgiac
200 lqedxgjac
200 wqedxgiac
200 lqeddgiac
200 lqzdxgiac
200 slovgevmwi
300 5 lqtdxgiac lqeddgiac lqedxgial lqedxgjac slovgevmwi
200 lqedrgiac
200 wlovgxvmwi
200 slovcxvmwi
200 lqedxgiac
200 dqedxgiac
200 spovgxvmwi
200 olovgxvmwi
200 jciedrbl
200 jciedzbf
200 lqeoxgiac
300 5 dqedxgiac alovgxvmwi jciedbbl slovgevmwi jciedzbf
200 lqedxgiqc
200 slovgxwmwi
200 slovgxvowi
300 5 dqedxgiac jciedbbl olovgxvmwi jciedzbf slovcxvmwi
200 slsvgxvmwi
200 slovyxvmwi
300 5 dqedxgiac olovgxvmwi slovcxvmwi jciedrbl jciedzbf
300 5 dqedxgiac olovgxvmwi slovcxvmwi jciedrbl jciedzbf
200 lqedxgiac
300 5 lqedxgiac olovgxvmwi slovcxvmwi jciedrbl jciedzbf
200 lqedxdiac
200 slvvgxvmwi
200 jciepzbl
200 jcgedzbl
200 slovgnvmwi
200 fciedzbl
300 5 lqedxgiac slovcxvmwi slsvgxvmwi fciedzbl jcgedzbl
200 slovgxvtwi
300 5 lqedxgiac slovgxvowi slsvgxvmwi fciedzbl jcgedzbl
200 uciedzbl
300 5 dqedxgiac fciedzbl slovgxvowi slsvgxvmwi jcgedzbl
200 slovgxvmii
200 slovgxvmwi
200 jcieazbl
200 jciedbbl
300 5 slovgnvmwi lqedxdiac fciedzbl jcieazbl jcgedzbl
121
100 20
300 0
200 bvtokss
200 vdsqtaja
200 nvtckss
200 vrclua
200 bvtckst
200 akhnn
200 rzmqgsjpss
200 vrcljh
200 achnn
200 masxef
200 krcfgmkogz
200 vrhlja
200 iduqtaja
200 uoamzbj
200 rzbqgsjbss
300 5 achnn bvtckst bvtokss iduqtaja krcfgmkogz
200 idsqtava
200 masxau
200 bfhnn
200 rzdqgsjbss
200 afhnc
200 masxaa
300 5 achnn masxaa rzbqgsjbss afhnc bfhnn
300 5 achnn masxaa rzbqgsjbss afhnc bfhnn
200 rzzqgsjbss
200 uoamzvj
300 5 rzbqgsjbss achnn masxaa uoamzbj afhnc
200 krcfnmkzgz
200 ramqgsjbss
300 5 rzbqgsjbss achnn masxaa uoamzbj afhnc
200 nrcfgmkzgz
200 zosbqoyypk
200 bvyckss
200 krcfvmkzgz
300 5 rzbqgsjbss krcfnmkzgz masxaa uoamzbj afhnc
200 zosbqdyypm
200 zosbqoxypm
200 aosbqoyypm
200 vrclfa
200 idhqtaja
200 vrcdja
200 joamzbj
200 idyyz
200 uoajzbj
200 bvackss
200 idsqtala
200 zasxaf
200 zosbqoyyhm
200 icyys
200 rzmqgsjbsf
300 5 bvackss aosbqoyypm icyys idhqtaja idsqtala
200 vrtlja
200 idsqtajv
200 pfhnn
200 fzmqgsjbss
200 uoavzbj
200 zosbqzyypm
200 vbclja
200 aftnn
300 5 uoajzbj aftnn bvackss fzmqgsjbss icyys
200 vrcyja
200 hfhnn
200 uozmzbj
200 bvtcksw
200 rzmqqsjbss
200 vtclja
200 krcfwmkzgz
200 idsqraja
200 bvtckks
200 bvtcksc
200 koamzbj
300 5 bvtcksc hfhnn vbclja aftnn bvtckks
200 afhmn
200 xdsqtaja
200 iayyz
200 krclja
200 rzmqgsjbss
200 afhnm
200 rzaqgsjbss
200 masxah
200 zosbqoyypm
300 5 rzaqgsjbss bvtcksc afhmn afhnm bvtckks
200 voclja
200 uoamzbc
200 iyyyz
300 5 rzaqgsjbss bvtcksc iayyz voclja afhmn
200 zosbqoyjpm
200 rzmqgsjfss
200 dasxaf
200 idsqeaja
200 vrclma
200 afknn
200 idsqsaja
300 5 rzaqgsjbss iayyz idsqeaja zosbqoyjpm afhmn
300 5 rzaqgsjbss iayyz idsqeaja zosbqoyjpm afhmn
200 krcffmkzgz
300 5 rzaqgsjbss iayyz idsqeaja zosbqoyjpm afhmn
200 vyclja
200 zosbqodypm
300 5 rzaqgsjbss zosbqodypm iayyz idsqeaja voclja
200 zosbqoyygm
200 idsqtajs
200 zasbqoyypm
200 uoauzbj
300 5 zasbqoyypm idsqeaja voclja afknn dasxaf
200 krclgmkzgz
200 rzmegsjbss
200 icyya
300 5 idsqeaja voclja afknn dasxaf icyya
300 5 idsqeaja voclja afknn dasxaf icyya
200 krcflmkzgz
200 uoamzbv
200 icxyz
200 icyaz
200 mysxaf
200 pcyyz
200 masxlf
200 bvtjkss
300 5 krcffmkzgz afknn bvtjkss icxyz icyaz
121
100 20
200 frniusu
200 lnwfowp
200 uelpcmoho
200 uoeeb
200 tjwfowp
200 efalivv
200 gptepu
200 pvfemyoj
200 caoce
200 nojtvbpes
200 fhueeibyko
200 uejpcmoho
200 pcfemyoq
200 hvieszl
200 fwvcdwage
200 uqbcjnsdn
200 ncjkvbpes
300 5 uejpcmoho caoce efalivv fhueeibyko frniusu
200 fkwpxxhqw
300 5 uejpcmoho caoce efalivv fhueeibyko fkwpxxhqw
200 xraiusu
200 oftgaz
200 pznjaes
200 uoeki
200 caoto
200 oznjyes
200 efadivc
200 fkwpxkhql
200 hodqzvgreq
300 5 caoce caoto efadivc fhueeibyko fkwpxkhql
200 ftccdwage
300 5 caoce caoto efadivc fhueeibyko fkwpxkhql
200 nojkvrpes
200 ubuqwnmu
300 5 caoto efadivc fhueeibyko fkwpxkhql fkwpxxhqw
200 ueudcmoho
200 cgoco
200 gsthpu
200 ueupymoho
200 caocy
300 5 caocy caoto cgoco efadivc fkwpxkhql
200 ftvcdwagq
200 wsppkzop
200 hosqzvgreq
200 nojkvjpes
200 ftmcdwage
200 wsppkzoj
200 qhuleibyko
200 wspskzop
300 5 wsppkzoj ftccdwage hodqzvgreq nojkvjpes caocy
200 ftvcdwlge
200 ubshwnmu
300 5 wsppkzoj ftccdwage hodqzvgreq nojkvjpes caocy
200 xrnkusu
200 hoiqqvgreq
200 ftvcdwagz
200 ftvcdwage
200 pesieyxum
300 5 ftmcdwage wsppkzoj caocy cgoco gsthpu
200 tnwfewp
200 uqmcjnsdw
200 pkgieyxum
300 5 ftmcdwage wsppkzoj caocy hoiqqvgreq hosqzvgreq
200 wfdgaz
200 pusieyxum
200 umbcjnsdw
200 nojkvbjes
200 wsppkzup
300 5 ftmcdwage pesieyxum hoiqqvgreq nojkvbjes nojkvjpes
200 pcfamyoj
200 oznjaeb
200 pcfemyaj
200 qaueeibyko
200 caico
200 cqoco
200 ueulcmoho
200 xryiusu
200 xrnihsu
200 oznjaew
200 tnwfowm
300 5 oznjaeb pesieyxum caico cqoco nojkvbjes
200 ubuhznmu
200 ubuhknmu
200 ftvcdwaye
200 ekalivc
200 hviearl
200 ftvcdwxge
200 gptipu
300 5 oznjaeb ubuhknmu caico cqoco ekalivc
200 pccemyoj
200 ubuhwnvu
300 5 oznjaeb ubuhknmu caico cqoco ekalivc
200 wsppkzop
200 fhwpxxhql
300 5 ubuhknmu caico cqoco ekalivc fhwpxxhql
200 ubuiwnmu
200 uoekb
200 uznjaes
300 5 ubuhknmu cqoco ekalivc fhwpxxhql ftvcdwaye
200 gpthpu
200 umuhwnmu
200 xrkiusu
300 5 gpthpu ubuhknmu ekalivc fhwpxxhql ftvcdwaye
200 fojkvbpes
200 fkwpxxhxl
200 efalivc
200 fkwpxxhqs
200 ftvcnwage
200 gpthmu
300 5 gpthmu efalivc fhwpxxhql fkwpxxhqs fkwpxxhxl
200 ftvsdwage
200 wsppkztp
200 efalidc
200 soiqzvgreq
200 tnwfowe
200 tnwfomp
300 5 efalidc gpthmu wsppkzop fhwpxxhql fkwpxxhqs
200 fkwpxxhql
200 wsppkzoy
300 5 fkwpxxhql efalidc gpthmu fojkvbpes ftvcnwage
251
100 50
300 0
200 ntzgk
200 ntigt
200 aqoxlrnrn
200 aqvxlrnrn
200 aqvxdrnrn
200 stigk
200 ntbgk
200 etigk
300 4 aqoxlrnrn etigk ntbgk ntigt
200 aqvxzrnrn
300 4 aqoxlrnrn etigk ntbgk ntigt
200 ntsgk
200 ntijk
200 rtigk
200 ctigk
200 iqvxlrnrn
200 htigk
200 aqsxlrnrn
200 ntigs
300 5 aqoxlrnrn ctigk ntbgk ntigs ntijk
200 aqvxlrnan
300 5 aqoxlrnrn ctigk ntbgk ntigs ntijk
200 ntihk
200 ntigs
200 ntpgk
200 aqvxlrnzn
200 jtigk
200 aqvxlrvrn
200 aqvxlcnrn
200 ntcgk
200 nvigk
200 aqvxlrlrn
200 aqgxlrnrn
300 5 aqgxlrnrn ctigk ntbgk ntigs ntihk
200 aqvzlrnrn
200 aqvxlrcrn
200 lqvxlrnrn
200 aqvxlsnrn
200 aqjxlrnrn
200 aqvxlrkrn
200 etigk
200 ntugk
200 aqvxlrntn
200 aqvxlrnin
200 aqvxwrnrn
300 5 aqgxlrnrn etigk ntbgk ntigs ntihk
300 5 aqgxlrnrn etigk ntbgk ntigs ntihk
200 aqvxlrwrn
200 ntigs
200 nxigk
200 aqvxlenrn
200 ntizk
300 5 aqgxlrnrn etigk ntbgk ntigs ntihk
200 aqvxrrnrn
200 ntigc
200 ntigk
200 ntige
200 aqvxdrnrn
200 aqvxlrvrn
300 2 aqvxdrnrn ntigs
200 ntigu
200 ntvgk
200 qqvxlrnrn
200 aqvxlrnrs
200 aqvxlrnrd
200 ntsgk
200 ntign
200 aqvxlrern
200 ntixk
200 ntogk
200 aqvxlrirn
200 ntirk
300 5 ntigs aqvxlrvrn aqvxlrnan aqgxlrnrn aqvxdrnrn
200 ntagk
300 5 ntigs aqvxlrvrn aqvxlrnan aqgxlrnrn aqvxdrnrn
200 cqvxlrnrn
300 5 ntigs aqvxlrvrn aqvxlrnan aqgxlrnrn aqvxdrnrn
200 aqsxlrnrn
200 neigk
200 awvxlrnrn
200 btigk
200 ntigu
300 5 ntigu aqvxlrvrn aqgxlrnrn aqvxdrnrn aqvxlcnrn
200 ntigd
200 aqvxlanrn
200 ntogk
200 neigk
200 ntmgk
200 itigk
200 ntixk
200 ntizk
200 aqvvlrnrn
300 5 neigk aqvxlrcrn aqvxdrnrn aqvxlanrn cqvxlrnrn
200 aqvxprnrn
200 utigk
200 aqvxhrnrn
200 nttgk
300 5 neigk aqvxdrnrn aqvxlrern aqjxlrnrn aqvxlanrn
300 5 neigk aqvxdrnrn aqvxlrern aqjxlrnrn aqvxlanrn
200 ntugk
200 aqvxlrnrn
200 aqvblrnrn
200 aqvllrnrn
200 aqvxlrnrn
200 mqvxlrnrn
200 aqvxzrnrn
200 ntiuk
200 aquxlrnrn
200 aqvxlrnrb
200 aqvxlknrn
200 ytigk
200 rtigk
300 2 neigk aqvxlrnrn
200 aqvxxrnrn
300 2 neigk aqvxlrnrn
200 aqwxlrnrn
200 aevxlrnrn
300 5 aqvxlrnrn ntogk btigk ntixk ntigu
300 5 aqvxlrnrn ntogk btigk ntixk ntigu
200 ntijk
200 ntigk
300 2 neigk aqvxlrnrn
200 nsigk
200 aqvxlrfrn
200 ptigk
200 aqvxlrurn
300 2 neigk aqvxlrnrn
200 eqvxlrnrn
300 2 neigk aqvxlrnrn
200 aqvxlrsrn
200 ntiok
200 ntiok
200 nvigk
200 aqxxlrnrn
200 ngigk
200 wtigk
200 aqvelrnrn
300 2 aqvxlrnrn neigk
200 ntfgk
200 ntigh
200 aqvxlrsrn
200 xtigk
200 aqvxlrnhn
200 aqvxlrkrn
200 xtigk
200 nxigk
200 aqvylrnrn
200 aqvxcrnrn
200 ntihk
200 azvxlrnrn
200 dtigk
200 aqvxprnrn
300 2 aqvxlrnrn ntiok
200 ntiga
200 ayvxlrnrn
200 aqhxlrnrn
200 aqvxlrnry
200 asvxlrnrn
200 ntigz
200 uqvxlrnrn
200 ntimk
200 naigk
200 aqhxlrnrn
200 aqvxhrnrn
200 advxlrnrn
200 niigk
200 aqvxlrnsn
200 noigk
200 aqvxvrnrn
200 aqvxlrnin
200 aivxlrnrn
200 ntiga
200 htigk
200 aqvxwrnrn
200 nmigk
200 aqvxlrnrm
200 nhigk
300 5 naigk xtigk advxlrnrn aqvxcrnrn aqvxlrsrn
200 aqvxlrnrv
200 ztigk
200 aqvxkrnrn
200 ntiek
200 ntngk
200 ncigk
200 nvigk
200 aqlxlrnrn
300 5 naigk aqvxcrnrn xtigk advxlrnrn aqhxlrnrn
300 5 naigk aqvxcrnrn xtigk advxlrnrn aqhxlrnrn
200 ntigl
300 5 naigk aqvxcrnrn xtigk advxlrnrn ntiga
200 ntige
200 aqvxlqnrn
200 ntqgk
200 aqvxlrnrx
200 aqvtlrnrn
200 ntink
300 5 naigk aqvxcrnrn advxlrnrn ntiga xtigk
200 nqvxlrnrn
300 5 naigk aqvxcrnrn advxlrnrn ntiga aqvxlrnrm
300 5 naigk aqvxcrnrn advxlrnrn ntiga aqvxlrnrm
200 noigk
300 5 noigk aqvxcrnrn advxlrnrn ntiga aqvxlrnrm
300 5 noigk aqvxcrnrn advxlrnrn ntiga aqvxlrnrm
200 aqvvlrnrn
200 ntigz
200 ntiek
300 5 noigk aqvxcrnrn ntiga advxlrnrn ntiek
300 5 noigk aqvxcrnrn ntiga advxlrnrn ntiek
200 etigk
300 5 noigk aqvxcrnrn ntiga advxlrnrn ntiek
200 ntiwk
300 5 noigk ntiek ntiga advxlrnrn aqvxhrnrn
200 ntigr
200 aqvxlsnrn
200 ntigw
200 aqzxlrnrn
200 ntigz
200 ntdgk
200 ntidk
200 aqvxarnrn
200 aqmxlrnrn
200 ntigr
200 aqvxurnrn
300 5 noigk ntigr aqvxarnrn ntiek aqhxlrnrn
300 5 noigk ntigr aqvxarnrn ntiek aqhxlrnrn
200 atigk
200 aqvxlrnsn
300 5 ntigr noigk aqvxarnrn ntiek aqhxlrnrn
300 5 ntigr noigk aqvxarnrn ntiek aqhxlrnrn
300 5 ntigr noigk aqvxarnrn ntiek aqhxlrnrn
300 5 ntigr noigk aqvxarnrn ntiek aqhxlrnrn
200 aqixlrnrn
200 ntdgk
200 aqvxlrnpn
200 nwigk
200 aqvxlrnqn
200 otigk
300 5 ntigr ncigk aqvxarnrn atigk ntiek
200 nqigk
200 aqvxlrnjn
300 5 ntigr ncigk atigk ntiek aqixlrnrn
200 aqvblrnrn
300 5 ntigr ncigk atigk ntiek aqixlrnrn
300 5 ntigr ncigk atigk ntiek aqixlrnrn
200 aqvxhrnrn
200 nmigk
200 abvxlrnrn
200 ntigh
300 5 ntigr ncigk ntiek aqixlrnrn aqvxarnrn
251
100 50
200 lvvyyuho
200 dkkqih
200 lvryynho
200 lvryyueo
200 lvryyuco
200 gojwpmwmuy
200 dkkqcc
300 5 lvryyuco dkkqcc dkkqih gojwpmwmuy lvryynho
200 grcwpmwmuy
300 5 lvryyuco dkkqcc dkkqih gojwpmwmuy grcwpmwmuy
200 vxjfinlzy
200 gocbpmwmuy
200 ixjfbnlzy
200 isisciwb
200 gocspmwmuy
300 5 gocbpmwmuy lvryyuco dkkqcc dkkqih gojwpmwmuy
200 lvnyyuho
200 lvryynho
200 dkkqik
200 vxjfbrlzy
300 5 dkkqih gocbpmwmuy lvnyyuho lvryynho lvryyuco
200 vxxfbnlzy
200 dkkqic
200 dkkqic
200 zxjfbnlzy
200 isikciwr
300 5 dkkqic gocbpmwmuy ixjfbnlzy lvnyyuho lvryynho
200 dkwqic
200 isigciwr
200 vxjfbnlzy
200 vxjfbnlby
200 lzryyuho
200 dkkqiv
300 5 dkkqic ixjfbnlzy gocbpmwmuy isigciwr lvnyyuho
300 5 dkkqic ixjfbnlzy gocbpmwmuy isigciwr lvnyyuho
200 igisciwr
200 vxjfbnlly
200 vxjfbflzy
200 vxhfbnlzy
200 gvcwpmwmuy
200 dkkqid
300 5 ixjfbnlzy dkkqic gocbpmwmuy grcwpmwmuy isigciwr
200 gocwpmwjuy
200 lvryyulo
200 vxjfbnlry
200 ifisciwr
200 lvrynuho
200 isiscilr
300 5 ixjfbnlzy dkkqic lvryyuco gocbpmwmuy grcwpmwmuy
200 dskqic
200 lvdyyuho
300 5 ixjfbnlzy dkkqic lvdyyuho lvryyuco gocbpmwmuy
200 lvryyudo
200 lmryyuho
200 isidciwr
200 isisciwd
200 dkkzic
300 5 ixjfbnlzy dkkqic lvryyuco isidciwr lvdyyuho
200 gocwpmwzuy
200 lvryygho
300 5 ixjfbnlzy dkkqic lvryyuco isidciwr lvdyyuho
200 gocwpmwmuy
200 lvryyuho
200 dkzqic
300 5 lvryynho ixjfbnlzy dkkqic gocbpmwmuy isidciwr
200 lvryyuhr
300 5 lmryyuho ixjfbnlzy dkkqic gocbpmwmuy isidciwr
200 lvryyuto
200 vhjfbnlzy
200 vxjfbxlzy
200 vxjfbqlzy
200 gochpmwmuy
200 isisciwb
200 isimciwr
200 isieciwr
200 gqcwpmwmuy
200 xsisciwr
200 vxjjbnlzy
200 dkkqnc
300 5 vhjfbnlzy dkkqic lmryyuho gochpmwmuy isidciwr
200 vhjfbnlzy
200 xkkqic
200 skkqic
200 isisclwr
200 gocwpgwmuy
200 lvryyuhf
200 isusciwr
200 dzkqic
200 godwpmwmuy
200 gocwpmwmhy
300 5 lmryyuho gochpmwmuy isidciwr vxjfbflzy vxjfbnlby
200 dkkqlc
200 dkkaic
300 5 lmryyuho gochpmwmuy isidciwr vxjfbflzy dkkaic
200 lvrjyuho
200 gocfpmwmuy
300 5 lmryyuho gocfpmwmuy isidciwr vxjfbflzy dkkaic
200 dkkaic
200 fkkqic
200 lvryuuho
200 dknqic
200 isiiciwr
200 lvryyuro
200 dkbqic
200 gocwpmwduy
200 lnryyuho
200 lvryyyho
200 gocwpmwyuy
200 gocwpmbmuy
200 lvrwyuho
200 gocwpmxmuy
300 5 gocfpmwmuy lmryyuho isidciwr dkbqic dkkaic
200 ibisciwr
200 ysisciwr
200 qxjfbnlzy
200 gocwpmemuy
300 5 gocfpmwmuy lnryyuho dkbqic fkkqic isieciwr
200 isiuciwr
300 5 gocfpmwmuy lnryyuho isieciwr dkbqic fkkqic
200 gocfpmwmuy
200 gocwpmwmul
200 gocwpmwmyy
200 lvryyugo
200 lvrwyuho
300 5 isieciwr fkkqic gocfpmwmuy gocwpmbmuy lvrwyuho
200 lvryyuhq
200 dkkqit
300 5 isieciwr fkkqic gocfpmwmuy gocwpmbmuy lvrwyuho
200 dckqic
200 dkwqic
200 lvryyuho
200 gocwpmwmuy
300 5 gocfpmwmuy lvrwyuho isieciwr dkbqic fkkqic
200 gocwpmwmby
200 dkkqtc
200 dkkqio
300 5 gocfpmwmuy lvrwyuho dkbqic dkkqlc fkkqic
200 istsciwr
300 5 gocfpmwmuy lvrwyuho dkbqic dkkqlc fkkqic
300 5 gocfpmwmuy lvrwyuho dkbqic dkkqlc fkkqic
200 dkuqic
200 lvryyujo
300 5 gocfpmwmuy lvrwyuho dkbqic fkkqic dckqic
200 vmjfbnlzy
200 evryyuho
200 wkkqic
200 vxjfanlzy
300 5 gocfpmwmuy lvrwyuho dkbqic dckqic dkkaic
200 isisciwr
200 isisiiwr
200 isistiwr
200 gocwpmwmvy
300 5 gocfpmwmuy lvrwyuho ibisciwr dkbqic dkkaic
200 istsciwr
200 ikisciwr
200 lvryydho
200 dkkvic
200 fkkqic
200 vxjrbnlzy
200 dkkqik
200 vxjpbnlzy
200 bvryyuho
200 gocwpmwpuy
200 ekkqic
200 exjfbnlzy
200 ghcwpmwmuy
300 5 ghcwpmwmuy lvrwyuho istsciwr dkkqik ekkqic
200 ivryyuho
300 5 ghcwpmwmuy lvrwyuho istsciwr dkkqik ekkqic
200 lvryyuho
200 vxofbnlzy
200 vxhfbnlzy
200 goowpmwmuy
200 gocwpmwmuv
200 gbcwpmwmuy
200 dkkoic
200 vxjfbnlky
200 lvwyyuho
200 isisciir
300 5 gbcwpmwmuy lvryyuho istsciwr dkkqik ekkqic
200 lvrdyuho
200 vxzfbnlzy
200 dkjqic
200 lvryyuho
300 5 lvryyuho gbcwpmwmuy istsciwr dkjqic dkkqik
200 vxjmbnlzy
200 vocwpmwmuy
200 fsisciwr
200 vxnfbnlzy
200 iqisciwr
200 dkkqik
200 vxjfbnldy
300 5 gbcwpmwmuy istsciwr lvryyuho vxhfbnlzy dkkqik
300 5 gbcwpmwmuy istsciwr lvryyuho vxhfbnlzy dkkqik
200 yxjfbnlzy
300 5 istsciwr lvryyuho vxhfbnlzy dkkqik ekkqic
200 gocwpmwmud
200 lvryyiho
200 vxjfbnlzr
200 gocwpmwmuf
300 5 lvryyuho fsisciwr vxhfbnlzy ekkqic gocwpmwmud
200 dzkqic
200 vijfbnlzy
200 gjcwpmwmuy
300 5 lvryyuho fsisciwr vxhfbnlzy ekkqic gbcwpmwmuy
200 isisaiwr
200 isdsciwr
200 dkeqic
200 dkxqic
300 5 lvryyuho vxhfbnlzy dkeqic gbcwpmwmuy gocwpmwmud
200 dkkqzc
200 dkfqic
200 vxjfbnlzy
300 5 exjfbnlzy lvryyuho dkeqic gbcwpmwmuy gocwpmwmud
300 5 exjfbnlzy lvryyuho dkeqic gbcwpmwmuy gocwpmwmud
200 lvmyyuho
200 tkkqic
200 vxjfbnezy
200 vxjmbnlzy
200 isisciwr
200 isigciwr
200 vxjfbnlzy
300 5 vxjfbnlzy lvryyuho fsisciwr dkeqic gbcwpmwmuy
300 5 vxjfbnlzy lvryyuho fsisciwr dkeqic gbcwpmwmuy
200 gocdpmwmuy
200 vxjfbnlzt
200 cxjfbnlzy
200 dmkqic
200 leryyuho
200 lvryygho
300 5 vxjfbnlzy lvryyuho fsisciwr dkeqic gocwpmwmud
300 5 vxjfbnlzy lvryyuho fsisciwr dkeqic gocwpmwmud
300 5 vxjfbnlzy lvryyuho fsisciwr dkeqic gocwpmwmud
200 vxjfbngzy
200 vxjfbnxzy
200 skkqic
300 5 vxjfbnlzy fsisciwr leryyuho dkeqic gocwpmwmud
200 isiscigr
200 hvryyuho
200 lwryyuho
200 dkkqmc
200 gocwpmwmry
300 5 vxjfbnlzy hvryyuho fsisciwr dkeqic dkkqmc
200 gwcwpmwmuy
200 gocwppwmuy
200 lvryjuho
200 lvxyyuho
200 lwryyuho
200 gocjpmwmuy
300 5 vxjfbnlzy lwryyuho fsisciwr dkeqic dkkqmc
251
100 50
200 hmdupa
200 ibqhpms
200 uoytsvu
200 yuoxbx
300 4 hmdupa ibqhpms uoytsvu yuoxbx
200 hqvbjojjf
200 jvkibfbm
200 uwytsvl
200 ibgbpms
200 uoftsvl
200 hxdula
200 zqdnbuxqvz
300 5 hmdupa hqvbjojjf hxdula ibgbpms ibqhpms
200 hqvbjomjf
200 jvkmbfbm
200 zjdnbuxovz
200 uoytnvl
200 wqlnex
200 pugxbx
300 5 hqvbjojjf jvkibfbm hmdupa hxdula ibgbpms
200 gmmmvc
200 dlxyk
200 dmwyk
200 yudxbx
200 hxdcpa
200 ibghpus
200 hqvbjoayf
300 5 hqvbjojjf jvkibfbm yudxbx dlxyk dmwyk
200 uoytsrl
300 5 hqvbjojjf jvkibfbm yudxbx dlxyk dmwyk
200 eilnex
200 dlzyk
200 gmfmvc
200 zqdnbuxkvz
200 eqinex
200 zqdnbuxokz
200 ihghpms
200 vmbmvc
200 gmblvc
200 eolnex
200 jvkzpfbm
200 dlwyt
200 uoytwvl
200 zqdnbsxovz
200 yugxbz
300 5 dlxyk eilnex gmfmvc hqvbjojjf jvkibfbm
300 5 dlxyk eilnex gmfmvc hqvbjojjf jvkibfbm
200 eqlner
200 uoyjsvl
200 uoatsvl
200 uobtsvl
200 jvkzffbm
300 5 uoatsvl dlxyk eilnex gmfmvc hqvbjojjf
200 hbvbjoajf
200 jvxzbfbm
200 hqlbjoajf
300 5 uoatsvl dlxyk eilnex gmfmvc hqvbjojjf
200 uoytsvl
200 kxdupa
200 ibgdpms
200 ubytsvl
200 ibdhpms
200 dlwhk
200 hxeupa
200 eqliex
200 dlwya
200 hxduga
200 eqlnyx
200 zqqnbuxovz
300 5 ubytsvl dlwya dlxyk eilnex gmfmvc
200 ivkzbfbm
200 zqdnbuxovh
200 rxdupa
200 jvkgbfbm
200 ibghpm
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
from collections import deque, defaultdict


# 최근 N개의 검색어
g_N = 0
window = deque()

# 현재 최근 N개 안에서 각 검색어 등장 횟수
keyword_count = {}

# pattern -> 현재 존재하는 검색어 집합
#
# ex)
# "aaa" -> "*aa", "a*a", "aa*"
#
# "*aa" : {"aaa", "baa", ...}
pattern_dict = defaultdict(set)


def get_patterns(word):
    """
    한 글자를 *로 치환한 모든 패턴 생성

    abc
    -> *bc
    -> a*c
    -> ab*
    """
    ret = []

    for i in range(len(word)):
        ret.append(
            word[:i] + "*" + word[i + 1:]
        )

    return ret


def activate_keyword(word):
    """
    최근 N개 안에 word가 처음 등장했을 때
    pattern_dict에 등록
    """
    for pattern in get_patterns(word):
        pattern_dict[pattern].add(word)


def deactivate_keyword(word):
    """
    최근 N개에서 word가 완전히 사라졌을 때
    pattern_dict에서 제거
    """
    for pattern in get_patterns(word):

        bucket = pattern_dict[pattern]

        bucket.remove(word)

        if not bucket:
            del pattern_dict[pattern]


def init(N: int) -> None:
    global g_N
    global window
    global keyword_count
    global pattern_dict

    g_N = N

    window = deque()

    keyword_count = {}

    pattern_dict = defaultdict(set)


def addKeyword(mKeyword: str) -> None:

    # =====================================================
    # 새로운 검색어 추가
    # =====================================================

    window.append(mKeyword)

    # 최근 N개에 처음 등장하는 검색어라면
    # 유사 검색용 pattern 등록
    if keyword_count.get(mKeyword, 0) == 0:
        activate_keyword(mKeyword)

    keyword_count[mKeyword] = keyword_count.get(mKeyword, 0) + 1


    # =====================================================
    # N개 초과 시 가장 오래된 검색어 제거
    # =====================================================

    if len(window) > g_N:

        old = window.popleft()

        keyword_count[old] -= 1

        # 최근 N개 안에서 완전히 사라진 경우
        if keyword_count[old] == 0:

            del keyword_count[old]

            deactivate_keyword(old)


def top5Keyword(mRet: List[str]) -> int:

    # 현재 존재하는 서로 다른 검색어들
    visited = set()

    # 이미 확인한 pattern
    #
    # 같은 pattern bucket을 여러 번 탐색할 필요가 없음
    used_pattern = set()

    # (그룹 총 등장횟수, 대표 검색어)
    groups = []


    # =====================================================
    # Connected Component 탐색
    # =====================================================

    for start in keyword_count:

        if start in visited:
            continue

        q = deque()

        q.append(start)
        visited.add(start)

        # 현재 component의 전체 호출 횟수
        total_count = 0

        # 대표 검색어
        representative = None
        representative_count = -1


        while q:

            cur = q.popleft()

            cur_count = keyword_count[cur]

            # ---------------------------------------------
            # 그룹 전체 등장 횟수
            # ---------------------------------------------

            total_count += cur_count


            # ---------------------------------------------
            # 대표 검색어 선정
            #
            # 1. 개별 등장 횟수가 많은 검색어
            # 2. 같으면 사전순
            # ---------------------------------------------

            if (
                cur_count > representative_count
                or
                (
                    cur_count == representative_count
                    and
                    cur < representative
                )
            ):
                representative = cur
                representative_count = cur_count


            # ---------------------------------------------
            # cur와 유사한 검색어 탐색
            # ---------------------------------------------

            for pattern in get_patterns(cur):

                if pattern in used_pattern:
                    continue

                used_pattern.add(pattern)

                # 같은 pattern을 가진 서로 다른 단어들은
                # 정확히 한 글자만 다름
                for nxt in pattern_dict[pattern]:

                    if nxt in visited:
                        continue

                    visited.add(nxt)
                    q.append(nxt)


        groups.append(
            (total_count, representative)
        )


    # =====================================================
    # 인기검색어 순위
    #
    # 1. 그룹 전체 등장 횟수 내림차순
    # 2. 대표 검색어 사전순
    # =====================================================

    groups.sort(
        key=lambda x: (-x[0], x[1])
    )


    # =====================================================
    # Top 5 반환
    # =====================================================

    ret_count = min(5, len(groups))

    for i in range(ret_count):
        mRet[i] = groups[i][1]

    return ret_count


# ── Main (수정 불가) ──
import sys
# (합쳐서 실행하므로 import 제거)

CMD_INIT = 100
CMD_ADD = 200
CMD_TOP = 300

def run():
    Q = int(input())
    okay = False
    for q in range(Q):
        input_iter = iter(input().split())
        cmd = int(next(input_iter))
        if cmd == CMD_INIT:
            N = int(next(input_iter))
            init(N)
            okay = True
        elif cmd == CMD_ADD:
            mKeyword = next(input_iter)
            addKeyword(mKeyword)
        elif cmd == CMD_TOP:
            mRet = [None for _ in range(5)]
            user_ans = top5Keyword(mRet)
            correct_ans = int(next(input_iter))
            if user_ans != correct_ans:
                okay = False
            for i in range(correct_ans):
                correct_keyword = next(input_iter)
                if correct_keyword != mRet[i]:
                    okay = False
        else:
            okay = False
    return okay


#sys.stdin = open('sample_input.txt', 'r')

T, MARK = map(int, input().split())

for tc in range(1, T + 1):
    score = MARK if run() else 0
    print("#%d %d" % (tc, score), flush = True)
