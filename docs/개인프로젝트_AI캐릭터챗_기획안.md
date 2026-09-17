# 개인 프로젝트 기획안

## When Does a Chat Become a Relationship?
### AI 캐릭터챗에서 대화 지속과 관계 형성을 만드는 상호작용 패턴 분석

## 1. 프로젝트 포지셔닝
이 프로젝트의 메인은 **스토리 생성이 아니라 Character / Companion Product**다.

스토리챗이 “다음 장면을 보고 싶게 만드는 서사적 몰입”을 중심으로 한다면, 캐릭터챗은 “이 캐릭터와 다음 대화를 계속하고 싶게 만드는 관계적 연속성”을 중심으로 한다.

본 프로젝트는 다음 흐름을 연결한다.

> **User Behavior → Product Hypothesis → Product Mechanism → Prototype / Eval → User Experiment**

1. **User Behavior** — 공개 대화 데이터에서 어떤 상호작용이 긴 대화·관계적 interaction과 함께 나타나는지 분석한다.
2. **Product Hypothesis** — 데이터에서 발견한 패턴을 제품 문제와 기능 가설로 번역한다.
3. **Product Mechanism** — 오픈소스 캐릭터챗을 통해 해당 기능이 실제로 어떤 구조로 구현되는지 이해한다.
4. **Prototype / Eval** — 핵심 문제 1개를 골라 Baseline vs Variant 형태로 검증한다.
5. **User Experiment** — 가능하면 실제 사용자 행동 실험으로 session continuation 또는 retention을 검증한다.

핵심 목표는 완성형 캐릭터챗 서비스를 직접 만드는 것이 아니라, **사용자 행동 데이터에서 출발해 제품 가설을 만들고, 실제 AI Product 구조와 실험으로 연결하는 것**이다.

---

## 2. 왜 AI Character / Companion을 선택했는가

### 2.1 사용자 행동과 제품 구조가 직접 연결되는 시장
캐릭터챗은 일반 정보 검색형 챗봇과 달리 사용자가 특정 캐릭터와 반복적으로 상호작용한다.

따라서 제품의 핵심 질문이 단순한 “정답 정확도”가 아니라 다음과 같이 바뀐다.

- 왜 어떤 대화는 짧게 끝나고 어떤 대화는 오래 이어지는가?
- 왜 특정 캐릭터와는 다시 대화하고 싶어지는가?
- Memory, Persona, Character Voice, Context Recall은 실제 경험에 어떤 차이를 만드는가?
- 관계의 연속성을 만드는 요소는 무엇인가?

이 구조는 **Engagement → Relationship → Retention → Monetization**으로 확장될 수 있어, 사용자 행동 데이터와 Product Decision을 연결하기에 적합하다.

### 2.2 실제 AI Product 문제를 다룰 수 있음
캐릭터챗은 단순히 LLM API를 연결하는 것만으로 완성되지 않는다.

실제 제품에서는 다음 문제가 중요하다.

- Persona Consistency
- Conversation Context
- Long-term Memory
- Retrieval
- Character Voice
- 자연스러운 한국어
- Latency / Cost / Quality Trade-off
- 관계 단계에 맞는 반응

따라서 데이터 분석 이후 실제 기술 구조와 Eval까지 연결하기 좋다.

### 2.3 데이터로 관찰 가능한 행동과 실험해야 할 행동을 분리할 수 있음
PIPPA와 같은 공개 conversation 데이터에서는 session 내 대화 지속과 interaction pattern을 분석할 수 있다.

반면 D1 / D7 Retention 같은 실제 재방문은 공개 데이터만으로 알 수 없다.

이 프로젝트는 이를 억지로 하나의 데이터셋에서 해결하지 않고,

> **공개 데이터 관찰 분석 → Product Hypothesis → Prototype / User Experiment**

으로 나누어 검증한다.

---

## 3. AI Companion 시장 분석

> 시장 규모 자료는 조사기관마다 AI Companion의 정의와 포함 범위가 다르므로 절대값보다 **성장 방향, 소비자 수요, 실제 서비스 지표**를 함께 본다.

### 3.1 글로벌 시장
Grand View Research는 글로벌 AI Companion 시장을 2025년 약 **368억 달러**, 2026년 약 **480억 달러**로 추정하며, 2033년 약 **3,180억 달러**까지 성장할 것으로 전망한다. 2026~2033년 예상 CAGR은 **31.0%**다.

또한 2025년 기준:

- Text-based AI Companion이 가장 큰 유형
- Social interaction & companionship이 가장 큰 application segment
- Consumer segment가 가장 큰 산업군
- North America가 가장 큰 시장
- Asia Pacific은 가장 빠르게 성장하는 지역으로 제시됨

Source: https://www.grandviewresearch.com/industry-analysis/ai-companion-market-report

실제 서비스 규모도 크다. Character.AI는 2025년 자사 기술 블로그에서 자사 서비스가 **월간 활성 사용자 2,000만 명 이상**을 지원한다고 밝혔다.

Source: https://blog.character.ai/harnessing-data-at-scale-character-ais-transition-to-warpstream/

앱 소비 측면에서도 2023~2024년 글로벌 AI Companion app 소비자 지출에서 미국이 30% 이상을 차지했고, 인도와 브라질도 큰 비중을 보였다.

Source: https://www.statista.com/statistics/1607445/top-markets-for-ai-companion-apps/

### 3.2 국내 시장
Grand View Research는 한국 AI Companion 시장을 2025년 약 **10.66억 달러**, 2033년 약 **81.10억 달러** 규모로 전망하며, 2026~2033년 CAGR을 **28.9%**로 제시한다.

Source: https://www.grandviewresearch.com/horizon/outlook/ai-companion-market/south-korea

다만 국내에서 더 직접적인 시장 신호는 실제 Character Chat 서비스의 성장에서 볼 수 있다.

2026년 서울경제 보도에 따르면:

- Scatter Lab의 **Zeta**는 누적 가입자 약 600만 명
- 2026년 5월 기준 국내 MAU 약 **140만 명**
- 일본에서는 주간 사용자 약 **75만 명**
- 일본 사용자의 평균 일일 사용시간은 약 **4시간**
- Scatter Lab은 전년도 매출 약 **260억 원**, 영업이익 약 **30억 원**을 기록
- Wrtn의 **Crack**은 2026년 5월 MAU 약 **55만 명**으로 전년 대비 두 배 이상 성장
- Wrtn은 일본에서 Charapu, 미국에서 OOC로 Character Chat 서비스를 확장 중

Source: https://en.sedaily.com/technology/2026/06/14/ai-chat-app-zeta-drives-scatter-lab-to-50-billion-won

국내 대형 IP 사업자도 Character Chat을 제품화하고 있다. 네이버웹툰은 작품 속 캐릭터와 일상대화 또는 롤플레잉을 할 수 있는 Character Chat 서비스를 운영하고 있으며, 메시지 구매 구조를 제공한다.

Source: https://help.naver.com/service/5635/contents/23251?lang=ko&osType=MOBILE

Wrtn의 Crack은 사용자 생성 캐릭터와 Creator 구조를 운영하며, Creator 조건에 캐릭터 수, 대화 사용자 수, 팔로워 수, 누적 발화 수 등을 사용하고 있다. 이는 Character Chat이 단순 AI 대화 기능을 넘어 **UGC / Creator Ecosystem**으로 확장되고 있음을 보여준다.

Source: https://help.crack.wrtn.ai/guide/creator/info/how-to-become

### 3.3 시장 구조 해석
현재 AI Character / Companion 시장은 하나의 형태가 아니라 다음과 같이 나뉠 수 있다.

| 유형 | 핵심 가치 | 주요 제품 문제 | 수익화 가능성 |
| --- | --- | --- | --- |
| Character Companion | 특정 캐릭터와의 관계·대화 | Persona, Memory, Voice | 구독, 메시지, premium model |
| IP Companion | 기존 IP 캐릭터와 상호작용 | Canon consistency, IP safety | 메시지, IP 소비, 굿즈 연계 |
| Fandom Companion | 팬덤 기반 반복 interaction | Personalization, exclusivity | 멤버십, 굿즈, digital item |
| Story / Roleplay | 서사 몰입과 다음 전개 | Plot, branching, pacing | 메시지, premium story |
| General Companion | 친구·생활 파트너형 대화 | Personalization, memory | 구독, premium features |

본 프로젝트는 이 중 **Character / Companion의 관계적 interaction과 session continuation**에 집중한다.

### 3.4 이 프로젝트가 보는 시장 기회
시장 규모 자체보다 본 프로젝트가 주목하는 것은 다음이다.

> **대화 품질이 단순 LLM 성능 경쟁에서 끝나는 것이 아니라, Memory / Persona / Voice / Relationship Continuity와 결합해 반복 사용을 만드는 제품 경쟁으로 이동하고 있는가?**

특히 국내 서비스가 일본·미국 등 해외로 확장하는 사례가 나타나고 있어, 한국어 Character Voice와 로컬라이제이션 품질 역시 중요한 Product Problem이 될 수 있다.

---

## 4. 핵심 문제 정의
AI 캐릭터챗에서 단순히 대화가 길다는 사실만으로 좋은 경험이라고 말할 수는 없다.

같은 30턴의 대화라도:

- 단순 Roleplay가 반복될 수 있다.
- 질문과 답변만 기계적으로 이어질 수 있다.
- 사용자가 점차 개인적인 이야기를 꺼낼 수 있다.
- 관계를 암시하는 표현이 증가할 수 있다.
- 캐릭터가 과거 맥락을 참조할 수 있다.
- 내용은 맞지만 번역체·AI 말투 때문에 캐릭터가 인간처럼 느껴지지 않을 수 있다.

따라서 메인 데이터 분석 질문은 다음과 같다.

> **긴 대화와 짧은 대화는 어떤 interaction 구조 차이를 보이는가?**

> **Conversation이 진행되면서 관계적 interaction은 어떻게 변화하는가?**

> **특정 AI response pattern 이후 session 내 conversation continuation은 어떻게 달라지는가?**

---

## 5. 데이터로 답할 질문

### Q1. 긴 대화와 짧은 대화는 어떤 차이가 있는가?
분석 후보:

- 사용자 / AI 메시지 길이
- 질문 빈도
- self-disclosure
- emotional expression
- personal preference sharing
- relational language
- 캐릭터별 차이

핵심은 **긴 conversation이 처음부터 다른지, 아니면 진행되면서 다른 interaction이 나타나는지** 확인하는 것이다.

### Q2. 대화가 진행되면서 관계적 interaction은 어떻게 변화하는가?
초기 taxonomy 후보:

- self-disclosure
- emotional expression
- relational language
- personal preference sharing
- past-context reference
- nickname / relationship naming
- future interaction reference

이를 early / middle / late 또는 turn percentile 기준으로 비교한다.

단, 실제 “관계가 깊어졌다”고 단정하지 않고 **관계적 interaction pattern의 변화**로 표현한다.

### Q3. 특정 AI 응답 이후 conversation continuation은 어떻게 달라지는가?
관찰 지표:

- next_turn 여부
- remaining_turns
- 이후 5턴 지속 여부
- 이후 10턴 지속 여부
- 사용자 메시지 길이 변화

여기서는 인과관계가 아니라 **association**만 분석한다.

---

## 6. 데이터로 알 수 없는 것
PIPPA만으로는 실제 **D1 / D7 Retention**을 알 수 없다.

동일 사용자가 다음날 다시 서비스에 방문했는지 추적할 수 없기 때문이다.

따라서:

> **Conversation Continuation ≠ Retention**

으로 구분한다.

또한 공개 conversation data만으로 “Memory 기능을 넣으면 retention이 증가한다”와 같은 인과적 결론을 내리지 않는다.

데이터 분석에서는:

> “특정 interaction pattern과 긴 conversation 사이에 association이 관찰되었다.”

까지 말하고, 그 다음 단계부터는 Product Hypothesis 또는 별도 Experiment로 분리한다.

---

## 7. 사용할 데이터

### 7.1 Primary Dataset — PIPPA
PIPPA는 Character.AI 사용자들이 자발적으로 제공한 실제 대화 로그 기반 공개 데이터셋이다.

- 약 26,000 conversation
- 100만 줄 이상의 dialogue
- 1,000개 이상의 character persona
- human / AI 발화 구분
- conversation sequence 보존

활용 목적:

- conversation depth
- turn-level continuation
- short vs long conversation
- progression
- character별 차이
- relationship interaction pattern

Source: https://huggingface.co/datasets/PygmalionAI/PIPPA

### 7.2 Validation Dataset — RP-Opus
최근 AI emotional companion / roleplay multi-turn 데이터.

활용 후보:

- PIPPA에서 발견한 패턴의 validation
- 한국어 subset 탐색
- 최근 companion interaction 비교

접근 또는 전처리 비용이 크면 메인 분석에서는 제외한다.

Source: https://huggingface.co/datasets/taozi555/rp-opus

### 7.3 Optional Eval Set — Korean Character Dialogue
한국어 Character Voice를 직접 검증할 필요가 생기면 소규모 Eval Set을 별도로 만든다.

평가 후보:

- 자연스러운 한국어 구어체
- 번역체 / 직역투 여부
- 캐릭터 고유 말투
- Persona Consistency
- Context Recall
- 과도한 설명체 / AI 어투
- 관계 단계에 맞는 반응

---

## 8. 분석 단위와 데이터마트
기본 분석 단위는 **Conversation**과 **Turn**이다.

| 분석 단위 | 예시 변수 |
| --- | --- |
| Conversation | conversation_id, character_id/name, total_turns |
| Turn | turn_number, speaker, message, message_length |
| Continuation | next_turn, remaining_turns, 5/10-turn continuation |
| Progression | early / middle / late, turn percentile |
| Interaction | 질문, 자기노출, 감정표현, 과거 맥락 참조 |
| Relationship | 관계적 표현, 호칭, future interaction reference |

1차 Conversation-Turn Mart 예시:

`conversation_id | character | turn_number | speaker | message | message_length | total_turns | next_turn | remaining_turns`

---

## 9. 분석 방법
방법론을 먼저 정하고 데이터를 끼워 맞추지 않는다.

### Phase 1 — Data Structure & EDA
- conversation 길이 분포
- turn 수 분포
- 사용자 / AI 메시지 길이
- 캐릭터별 conversation 수
- short vs long conversation 비교
- 민감 콘텐츠 / 제외 기준 확인

### Phase 2 — Turn-level Continuation
- next turn
- remaining turns
- 이후 5/10턴 지속 여부
- 사용자 참여 강도 변화

### Phase 3 — Conversation Progression
- early / middle / late 비교
- interaction pattern 변화

### Phase 4 — Relationship Interaction Analysis
- taxonomy 정의
- sample labeling
- 필요 시 LLM-assisted classification + human validation

### Phase 5 — Product Translation

> **Data Finding → Product Problem → Technical Mechanism → Feature Hypothesis → Eval Candidate**

분석 도구 후보:

- SQL
- Python / pandas
- 통계 검정
- 필요 시 Survival analysis
- 필요 시 sequence / clustering
- 시각화

분석의 목표는 복잡한 모델을 사용하는 것이 아니라 **제품 의사결정에 의미 있는 패턴을 찾는 것**이다.

---

## 10. AI Product Understanding — 오픈소스 캐릭터챗 구조 분석
완성형 캐릭터챗 개발이 아니라, 공개 오픈소스를 통해 실제 제품 구조를 이해한다.

분석 후보:

- RisuAI
- SillyTavern
- a16z Companion App
- OpenPersona

모든 프로젝트를 동일한 깊이로 보지 않고 1~2개를 메인으로 본다.

확인할 질문:

1. Character Persona는 어떻게 정의·주입되는가?
2. Conversation Context는 어떻게 유지되는가?
3. 장기 Memory는 무엇을 저장하는가?
4. 관련 Memory는 언제 retrieval되는가?
5. Persona Consistency는 어떻게 유지되는가?
6. Context Window 한계는 어떻게 처리하는가?
7. Character Voice는 어떻게 제어하는가?
8. Quality / Latency / Cost Trade-off는 무엇인가?

산출물:

- 캐릭터챗 시스템 구조도
- Persona / Prompt / Context / Memory / Retrieval 비교
- Data Finding ↔ Technical Mechanism 연결표

---

## 11. Product Hypothesis
분석 결과를 기능 가설로 연결한다.

예시:

> 과거 맥락 참조 interaction에서 더 긴 conversation이 관찰됨
> → Relationship Continuity가 중요한 Product Problem일 가능성
> → Memory Retrieval / Context Injection 구조 분석
> → Relationship Memory Hypothesis

또는:

> 특정 persona의 interaction이 상대적으로 오래 지속됨
> → Character Voice / Persona Consistency 가설
> → Prompt / Few-shot dialogue / style constraint 비교

---

## 12. Optional Prototype / Eval
메인 분석 결과에서 가장 중요한 문제 **1개만** 선택한다.

후보:

- Relationship Memory
- Character Voice / Natural Korean
- Persona Consistency
- Context Recall

실험 구조:

> **Problem Definition → Success / Failure Criteria → Test Set → Baseline vs Variant → Failure Analysis → Product Decision**

예: Character Voice

Baseline:
- 기본 Character Persona Prompt

Variant:
- 한국어 구어체 규칙
- Character-specific 말투
- Few-shot dialogue examples
- 번역체 방지 지침

Eval:
- 한국어 자연스러움
- 번역체 여부
- 캐릭터성
- Persona Consistency
- 문맥 적합성
- 다시 대화하고 싶은 정도

완성형 앱이 아니라 **검증용 실험 환경**을 만드는 것이 목표다.

---

## 13. Optional User Experiment — Retention
실제 retention을 검증하려면 동일 사용자의 재방문 데이터를 직접 만들어야 한다.

예시:

**Day 0**
- Character Chat 첫 사용

**D1 / D3 / D7**
- 재방문 여부 확인

비교 후보:

- Baseline Character
- Memory / Character Voice 개선 Variant

측정 후보:

- session turns
- session length
- D1 return
- D3 / D7 return
- 다시 대화할 의향
- 캐릭터 선호 / 애착

사용자 수가 충분하지 않으면 exploratory experiment로만 해석한다.

---

## 14. 한국어 Character Voice 문제
별도 Product Quality Track으로 둔다.

핵심 문제:

> **문법적으로 틀리지는 않지만 번역체·설명체·AI 말투 때문에 인간 또는 캐릭터처럼 느껴지지 않는 문제**

Failure Pattern 후보:

- 직역투
- 과도한 완전문
- 부자연스러운 대명사 사용
- 한국인이 잘 쓰지 않는 표현
- 과도한 설명
- 캐릭터 간 말투 동질화
- 설정과 다른 존댓말 / 반말
- 감정 상황과 맞지 않는 문장 길이

PIPPA 메인 데이터 분석과 분리해 한국어 Eval Track으로 다룬다.

---

## 15. Story Chat과의 차이
스토리챗은 이번 프로젝트의 메인이 아니다.

| Character / Companion | Story Chat |
| --- | --- |
| 관계 지속 | 서사 몰입 |
| 왜 다시 말하고 싶은가 | 왜 다음 장면을 보고 싶은가 |
| Memory | Narrative |
| Persona | World Building |
| Character Voice | Plot / Pacing |
| Relationship Continuity | Story Progression |

Story Chat 비교는 메인 프로젝트 완료 후 별도 후속 분석으로 분리한다.

---

## 16. 중간발표 및 실행 일정
중간발표: **2026-09-29**

### 9/17–9/19
- PIPPA 구조 확인
- Python 로딩
- 샘플 데이터 확인
- Conversation-Turn Mart 설계

### 9/20–9/22
- 전처리
- 기본 EDA
- conversation 길이 / turn / message length / character 분포
- short / long conversation 기준 설정

### 9/23–9/25
- Q1 분석
- 긴 conversation과 짧은 conversation 비교
- Q2 progression 1차 분석

### 9/26
- Relationship interaction taxonomy 초안
- sample labeling

### 9/27
- Turn-level continuation 1차 분석
- 중간 인사이트 선정

### 9/28
- 중간발표 자료 정리

### 9/29 — 중간발표
발표 범위:

1. 프로젝트 선택 이유 + 시장 배경
2. 데이터 구조
3. Conversation-Turn Mart
4. EDA 2~3개
5. 1차 분석 결과 1개 이상
6. 이후 Product Hypothesis / Prototype 계획

### 9/30 이후
- Relationship interaction 분석 고도화
- 오픈소스 구조 분석
- Product Hypothesis 도출
- 핵심 기능 1개 Eval / Prototype
- 가능하면 User Experiment

---

## 17. 프로젝트 범위 원칙
- 메인 제품 범주는 **Character / Companion**으로 고정한다.
- 메인 데이터는 PIPPA로 고정한다.
- RP-Opus는 Validation / Korean Quality Track 후보로 둔다.
- Conversation Continuation을 Retention이라고 부르지 않는다.
- 공개 데이터에서는 association까지만 말한다.
- Retention은 별도 User Experiment에서만 검증한다.
- 결제 데이터가 없으므로 Monetization 효과를 입증했다고 주장하지 않는다.
- 오픈소스 분석은 구조 이해가 목적이며 완성형 서비스를 만들지 않는다.
- Prototype / Eval은 핵심 문제 1개만 선택한다.
- Story Chat은 후속 프로젝트로 분리한다.
- NSFW / 민감 콘텐츠는 분석 목적에 필요하지 않으면 제외한다.

---

## 18. 프로젝트 독립성 및 출처 원칙
본 프로젝트는 **공개 데이터셋, 공개 오픈소스, 공개 문헌만 사용해 독립적으로 수행한다.**

이전 근무지의 내부 데이터, 비공개 기획 문서, Prompt, KPI, 정책, 코드 또는 confidential information은 사용하지 않는다.

시장 규모는 조사기관마다 정의가 다를 수 있으므로 단일 수치를 확정적 사실로 취급하지 않고, 출처와 기준연도를 함께 표기한다.

---

## 19. 프로젝트 완료 기준
1차 완료 기준:

1. 재현 가능한 Conversation-Turn Mart가 있다.
2. 최소 1개의 명확한 conversation continuation / engagement pattern을 설명할 수 있다.
3. Relationship interaction과 단순 conversation length를 구분해 해석한다.
4. 분석 결과를 최소 1개의 Product Problem으로 번역한다.
5. 해당 Product Problem이 실제 캐릭터챗 구조의 어떤 Mechanism과 연결되는지 설명한다.
6. 데이터가 말하는 것과 추정 / 가설을 구분한다.
7. 최종 Case Study에서 **문제 정의 → 데이터 분석 → 해석 → Product Hypothesis → Product Decision** 흐름이 보인다.

이 기준을 충족한 뒤에만 추가 데이터, Story Chat 비교, Prototype 또는 Retention Experiment로 확장한다.
