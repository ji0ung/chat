# 개인 프로젝트 기획안

## When Does a Chat Become a Relationship?
### AI 캐릭터챗에서 대화 지속과 관계 형성을 만드는 상호작용 패턴 분석

## 1. 프로젝트 포지셔닝
이 프로젝트의 메인은 **스토리 생성이 아니라 Character / Companion Product**다.

스토리챗이 “다음 장면을 보고 싶게 만드는 서사적 몰입”을 중심으로 한다면, 캐릭터챗은 “이 캐릭터와 다음 대화를 계속하고 싶게 만드는 관계적 연속성”을 중심으로 한다.

본 프로젝트는 다음 3개 층을 연결한다.

> **User Behavior → Product Mechanism → Product Decision**

1. **User Behavior** — 어떤 상호작용이 대화를 지속시키는가?
2. **Product Mechanism** — 그 경험은 실제 캐릭터챗에서 어떤 구조로 구현되는가?
3. **Product Decision** — 어떤 기능을 우선 개선하거나 검증할 가치가 있는가?

핵심 목표는 캐릭터챗을 완성형으로 직접 개발하는 것이 아니라, **사용자 행동 데이터와 실제 AI Product 구조를 연결해 제품 가설을 만드는 것**이다.

---

## 2. 핵심 문제 정의
AI 캐릭터챗에서 단순히 대화가 길다는 사실만으로 좋은 경험이라고 말할 수는 없다.

같은 30턴의 대화라도:

- 단순 Roleplay가 반복될 수 있다.
- 질문과 답변만 기계적으로 이어질 수 있다.
- 사용자가 점차 개인적인 이야기를 꺼낼 수 있다.
- 캐릭터가 이전 대화를 기억하며 관계가 이어지는 느낌을 줄 수 있다.
- 내용은 맞지만 번역체·AI 말투 때문에 캐릭터가 인간처럼 느껴지지 않을 수 있다.

따라서 본 프로젝트의 핵심 질문은 다음과 같다.

> **대화를 오래 지속시키는 상호작용과 관계 형성을 만드는 상호작용은 같은가?**

그리고 Product 관점에서는 한 단계 더 나아간다.

> **사용자가 ‘이 캐릭터와 관계가 이어지고 있다’고 느끼게 만드는 제품 메커니즘은 무엇인가?**

---

## 3. Research Questions

### 3.1 Behavior / Engagement
1. 어떤 AI 응답 이후 사용자의 대화가 더 오래 지속되는가?
2. 대화 초반과 후반의 사용자 행동은 어떻게 달라지는가?
3. 짧은 대화와 긴 대화는 어떤 구조적 차이를 보이는가?
4. 캐릭터별로 대화 지속 패턴에 차이가 있는가?
5. 특정 interaction pattern 이후 continuation probability가 달라지는가?

### 3.2 Relationship
6. 대화 지속성과 관계적 상호작용은 함께 증가하는가, 아니면 별개의 축인가?
7. 개인 정보 공유, 과거 대화 참조, 감정 표현, 관계 호칭과 같은 패턴은 대화 progression에 따라 어떻게 달라지는가?
8. 관계의 연속성을 느끼게 하는 interaction은 어떤 특징을 갖는가?

### 3.3 AI Product Quality
9. Persona Consistency와 Context Recall은 관계적 경험을 만드는 데 어떤 역할을 하는가?
10. 자연스러운 구어체와 캐릭터 고유 말투는 캐릭터 몰입에 어떤 영향을 줄 가능성이 있는가?
11. 문법적으로는 맞지만 번역체·AI 말투처럼 느껴지는 응답은 어떤 failure pattern으로 정의할 수 있는가?

※ 한국어 자연스러움은 PIPPA만으로 직접 검증하기 어렵기 때문에, **RP-Opus의 한국어 subset 또는 별도의 소규모 Eval Set**을 활용하는 확장 트랙으로 둔다.

---

## 4. 분석 단위
기본 분석 단위는 **Conversation**과 **Turn**이다.

| 분석 단위 | 예시 변수 |
| --- | --- |
| Conversation | conversation_id, character_id/name, total_turns |
| Turn | turn_number, speaker, message, message_length |
| Continuation | next_turn 여부, remaining_turns, 이후 5/10턴 지속 여부 |
| Progression | 초반/중반/후반 또는 turn percentile |
| Interaction | 질문, 자기노출, 감정표현, 과거 맥락 참조 등 |
| Relationship | 관계적 표현, 친밀도 관련 라벨 또는 패턴 |

관계성 스코어링 기준, 세부 라벨 정의, 가중치는 분석자가 직접 설계한다. 단, EDA 전에 임의의 단일 점수로 관계성을 고정하지 않는다.

---

## 5. 사용할 데이터

### 5.1 Primary Dataset — PIPPA
PIPPA는 Character.AI 사용자들이 자발적으로 제공한 실제 대화 로그를 모은 공개 데이터셋이다. 약 26,000개 conversation과 100만 줄 이상의 dialogue를 포함하고, 1,000개 이상의 캐릭터 persona가 포함된다.

대화 전체 sequence와 human/AI 발화 구분이 가능해 turn-level 분석에 적합하다.

- 활용 목적: conversation depth, turn continuation, character별 차이, progression 분석
- 장점: 충분한 규모, 실제 Character.AI 대화, sequence 보존
- 한계: 2023년 데이터, 자발적 제출 데이터, NSFW/민감 콘텐츠 일부 포함 가능
- Source: https://huggingface.co/datasets/PygmalionAI/PIPPA

### 5.2 Validation Dataset — RP-Opus
RP-Opus는 2026년 공개된 AI emotional companion/roleplay 대화 데이터셋이다. 대화당 4~60턴, user/assistant message sequence, 캐릭터명, 생성일시 등을 제공하며 한국어를 포함한 다국어 데이터가 있다.

- 활용 목적: PIPPA에서 발견한 패턴의 최근 데이터 검증, 한국어 품질 탐색 후보
- 장점: 2026년 데이터, multi-turn, 한국어 포함
- 한계: gated access, CC BY-NC 4.0, 개인 연구/포트폴리오 용도 중심
- Source: https://huggingface.co/datasets/taozi555/rp-opus

### 5.3 Optional Eval Set — Korean Character Dialogue
한국어 자연스러움이나 Character Voice 문제를 직접 검증할 필요가 생기면 소규모 Eval Set을 별도로 만든다.

예시 평가 축:
- 자연스러운 한국어 구어체
- 번역체 / 직역투 여부
- 캐릭터 고유 말투 유지
- Persona Consistency
- 이전 맥락 Recall
- 과도한 설명체 / AI 어투
- 관계 단계에 맞는 반응

이 Eval Set은 메인 데이터 분석과 분리하며, 필요 시에만 수행한다.

---

## 6. 분석 방향

### Phase 1 — Data Structure & EDA
- conversation 길이 분포
- turn 수 분포
- 사용자 / AI 메시지 길이
- 캐릭터별 conversation 수
- short vs long conversation 구조 비교
- 민감 콘텐츠 및 분석 제외 기준 확인

### Phase 2 — Turn-level Product Analysis
각 AI 응답 이후:

- 사용자가 다음 턴을 이어가는지
- 이후 몇 턴이 더 지속되는지
- 이후 5/10턴까지 이어지는지
- 사용자 메시지 길이와 참여 강도가 어떻게 변하는지

를 분석한다.

### Phase 3 — Conversation Progression
대화를 초반 / 중반 / 후반 또는 turn percentile로 나눠 interaction pattern이 시간에 따라 어떻게 달라지는지 본다.

### Phase 4 — Relationship Analysis
관계 관련 interaction taxonomy를 정의한 뒤, 대화 지속성과 관계 형성이 동일한 현상인지 서로 다른 축인지 확인한다.

초기 후보:
- self-disclosure
- emotional expression
- relational language
- personal preference sharing
- past-context reference
- nickname / relationship naming
- future interaction reference

### Phase 5 — Product Translation
분석 결과를 다음 프레임으로 연결한다.

> **Data Finding → Product Problem → Technical Mechanism → Feature Hypothesis → Eval Candidate**

예시:

> 과거 맥락을 이어받는 응답 이후 continuation이 높다
> → 관계 연속성이 engagement에 영향을 줄 가능성
> → Memory Retrieval / Context Injection 구조 확인
> → Relationship Memory 기능 가설
> → Recall / Naturalness / Persona Consistency Eval

---

## 7. 분석 방법 후보
방법론을 먼저 정하고 데이터를 끼워 맞추지 않는다. EDA 이후 Research Question에 필요한 수준으로 선택한다.

- SQL / Python 기반 Conversation-Turn Mart 생성
- 분포 비교 및 통계 검정
- Turn-level continuation analysis
- Survival analysis
- Conversation progression analysis
- 필요 시 clustering 또는 sequence analysis
- 필요 시 텍스트 라벨링 / LLM-assisted classification + human validation
- 시각화: turn depth, continuation curve, character별 패턴, progression chart

분석의 목표는 복잡한 모델을 사용하는 것이 아니라 **제품 의사결정에 의미 있는 차이를 찾는 것**이다.

---

## 8. AI Product Understanding — 오픈소스 캐릭터챗 구조 분석

### 8.1 목적
완성형 캐릭터챗을 직접 개발하는 것이 아니라, 공개된 오픈소스 프로젝트를 통해 **캐릭터챗의 실제 제품·기술 구조를 이해하고 데이터 분석 결과를 구현 가능한 Product Hypothesis로 연결한다.**

### 8.2 분석 대상 후보
- **RisuAI** — Persona / Lorebook / Memory / Prompt 구조
- **SillyTavern** — Character Card / Context / Memory 확장 구조
- **a16z Companion App** — Retrieval + Memory 기반 최소 Companion 구조
- **OpenPersona** — Persona / Memory / Voice 구조 참고

모든 프로젝트를 동일한 깊이로 분석하지 않는다. 1~2개를 메인으로 보고 나머지는 비교 참고용으로 사용한다.

### 8.3 확인할 질문
1. Character Persona는 어떻게 정의되고 LLM 입력에 주입되는가?
2. Conversation Context는 어떤 방식으로 유지되는가?
3. 장기 Memory는 무엇을 저장하고 언제 retrieval하는가?
4. Persona Consistency는 어떤 구조로 유지되는가?
5. Context Window 한계는 어떻게 처리하는가?
6. Prompt는 어떤 구성 요소로 조립되는가?
7. 자연스러운 Character Voice를 유지하기 위해 어떤 제어가 가능한가?
8. 품질·Latency·Cost 사이에는 어떤 trade-off가 있는가?
9. 데이터 분석에서 발견한 interaction pattern을 실제 기능으로 구현하려면 어떤 기술 메커니즘이 필요한가?

### 8.4 산출물
- 캐릭터챗 핵심 시스템 구조도
- Persona / Prompt / Context / Memory / Retrieval 구성요소 정리
- 오픈소스 프로젝트별 구현 접근 비교
- Data Finding ↔ Technical Mechanism 연결표
- 우선 검증할 Product Hypothesis 도출

---

## 9. Optional AI PM Experiment — 핵심 기능 1개 Eval
메인 분석 결과에서 명확한 Product Problem이 발견된 경우에만 수행한다.

후보 예시:
- Relationship Memory
- Character Voice / Natural Korean
- Persona Consistency
- Context Recall

실험 구조:

> **Problem Definition → Success / Failure Criteria → Test Set → Variant Comparison → Failure Analysis → Product Decision**

예: Character Voice를 선택한 경우

- Baseline: 일반적인 캐릭터 Prompt
- Variant: 한국어 구어체 / 말투 규칙 / persona example 강화
- Eval: 자연스러움, 번역체 여부, 캐릭터성, 문맥 적합성
- 결과: 품질 개선 폭과 Prompt 복잡도 / 비용 / 유지보수 Trade-off 정리

완성형 서비스 구현보다 **AI 기능의 품질 기준을 정의하고 의사결정하는 과정**을 보여주는 것이 목적이다.

---

## 10. 20일 실행 계획

| 기간 | 작업 |
| --- | --- |
| Day 1–2 | PIPPA / RP-Opus 구조 확인, 샘플링, 제외 기준 및 분석 범위 확정 |
| Day 3–5 | 전처리 및 Conversation-Turn Mart 생성 |
| Day 6–8 | EDA: 길이·턴·캐릭터·short/long conversation 분석 |
| Day 9–11 | Turn-level continuation 분석 |
| Day 12–13 | Conversation progression 분석 |
| Day 14–15 | Relationship interaction taxonomy 정의 및 분석 |
| Day 16 | 오픈소스 캐릭터챗 구조 분석 |
| Day 17 | Data Finding → Product Mechanism 연결 및 Feature Hypothesis 도출 |
| Day 18 | 핵심 가설 1개 Eval 설계 또는 추가 분석 |
| Day 19 | 시각화 / 대시보드 / 구조도 정리 |
| Day 20 | 포트폴리오 문서화 및 QA |

※ 실제 데이터 품질에 따라 Phase의 깊이는 조정하되, **20일 내 Main Analysis 완성**을 우선한다.

---

## 11. 기대 산출물

### Data Analysis
- Conversation / Turn 분석 데이터마트
- 캐릭터챗 대화 지속 구조 EDA
- Turn-level continuation analysis
- Conversation progression analysis
- 관계적 interaction과 engagement의 관계 해석

### AI Product Understanding
- 캐릭터챗 시스템 구조도
- Persona / Context / Memory / Retrieval 분석
- 오픈소스 구조 비교
- 품질 Failure Pattern 정리

### Product Output
- Product Insight
- Feature Hypothesis
- 우선순위가 높은 Product Problem 1개
- 필요 시 Eval Framework / Prototype 결과
- 포트폴리오 Case Study

---

## 12. Product 관점의 최종 질문

> **캐릭터챗에서 사용자를 오래 머물게 하는 것은 단순히 ‘재미있는 대답’인가, 아니면 ‘관계가 이어지고 있다고 느끼게 하는 경험’인가?**

그리고 그 경험을 만드는 요소를 다음과 같은 제품 가설로 연결한다.

- Memory
- Personalization
- Character Consistency
- Character Voice / Natural Language Quality
- Conversation Design
- Relationship Continuity

---

## 13. 후속 분석 — Immersion vs Relationship
스토리챗은 본 프로젝트의 메인이 아니다. 메인 캐릭터챗 프로젝트를 완성한 뒤, 필요할 경우 비교 연구로만 확장한다.

캐릭터챗이 **관계의 연속성**으로 지속 사용을 만든다면, 스토리챗은 **다음 전개에 대한 몰입과 선택의 연속성**으로 지속 사용을 만들 수 있다.

| 축 | 캐릭터 / Companion | Story Chat |
| --- | --- | --- |
| 핵심 경험 | 관계 / 상호작용 지속 | 서사 / 다음 전개 몰입 |
| 핵심 질문 | 왜 이 캐릭터와 다시 대화하는가? | 왜 다음 장면으로 넘어가는가? |
| 행동 단위 | Conversation Turn | Decision Event / Story Progression |
| 주요 공개 데이터 | PIPPA, RP-Opus | Rushes |
| 핵심 제품 문제 | Memory, Persona, Voice, Relationship | Narrative, Branching, Pacing, World Consistency |

Microsoft Research의 Rushes는 interactive narrative 분석 후보 데이터로 두되, 메인 20일 프로젝트에서는 분석하지 않는다.

- Source: https://www.microsoft.com/en-us/research/publication/rushes-a-human-preference-dataset-for-pluralistic-alignment/

---

## 14. 프로젝트 범위 원칙
- 메인 제품 범주는 **Character / Companion**으로 고정한다.
- 20일 내 Main Analysis 완성을 우선한다.
- 메인 데이터는 PIPPA로 고정한다.
- RP-Opus는 Validation 또는 한국어 품질 탐색용이며, 접근·전처리 비용이 크면 제외한다.
- 관계성은 사전에 임의의 단일 Score로 고정하지 않는다.
- 결제 데이터가 없으므로 과금 효과를 직접 입증했다고 주장하지 않는다.
- Monetization은 Product Hypothesis 수준에서만 연결한다.
- 오픈소스 분석은 제품·기술 구조 이해를 목적으로 하며, 완성형 캐릭터챗 구현은 하지 않는다.
- Prototype / Eval은 핵심 문제 1개가 명확해질 때만 수행한다.
- Story Chat 분석은 별도 후속 프로젝트로 분리한다.
- NSFW / 민감 콘텐츠는 분석 목적에 필요하지 않으면 제외하거나 별도 처리한다.

---

## 15. 프로젝트 독립성 및 출처 원칙
본 프로젝트는 **공개 데이터셋, 공개 오픈소스, 공개 문헌만 사용해 독립적으로 수행한다.**

이전 근무지의 내부 데이터, 비공개 기획 문서, 프롬프트, KPI, 정책, 코드 또는 기타 confidential information은 사용하지 않는다.

프로젝트의 분석 질문과 Product Hypothesis는 공개 자료와 본 프로젝트에서 직접 수행한 분석 결과를 기반으로 도출한다.

---

## 16. 프로젝트 완료 기준
이 프로젝트는 아래 조건을 충족하면 1차 완료로 본다.

1. 재현 가능한 Conversation-Turn Mart가 있다.
2. 최소 1개의 명확한 Engagement / Continuation 패턴을 설명할 수 있다.
3. Relationship interaction과 단순 conversation length를 구분해 해석한다.
4. 분석 결과를 최소 1개의 Product Problem으로 번역한다.
5. 해당 Problem이 실제 캐릭터챗 구조에서 어떤 Mechanism과 연결되는지 설명한다.
6. 데이터가 말하는 것과 추정 / 가설을 명확히 구분한다.
7. 최종 Case Study에서 **문제 정의 → 분석 → 해석 → Product Decision** 흐름이 보인다.

이 기준을 충족한 뒤에만 추가 데이터, Story Chat 비교, Prototype 또는 Eval로 확장한다.
