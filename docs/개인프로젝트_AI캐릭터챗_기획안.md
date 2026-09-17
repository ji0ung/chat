# 개인 프로젝트 기획안

## When Does a Chat Become a Relationship?
### AI 캐릭터챗에서 대화 지속과 관계 형성을 만드는 상호작용 패턴 분석

## 1. 프로젝트 개요
AI 캐릭터챗은 정보 검색형 챗봇과 달리, 사용자가 특정 캐릭터와 반복적으로 대화를 이어가며 감정적·관계적 경험을 형성하는 프로덕트다.

본 프로젝트는 캐릭터챗의 핵심 행동 단위를 클릭이나 구매가 아니라 **Conversation Turn**으로 보고, 어떤 상호작용이 대화를 지속시키고 대화가 진행되면서 관계적 상호작용이 어떻게 나타나는지 분석한다.

이번 20일 프로젝트의 목표는 결제까지 직접 검증하는 것이 아니다. 먼저 캐릭터챗 안에서 지속 사용의 핵심 메커니즘이 무엇인지 확인하고, 이후 과금·구독·스토리챗과의 비교로 확장 가능한 분석 기반을 만드는 데 초점을 둔다.

## 2. 핵심 문제 정의
같은 30턴의 대화라도 의미는 다를 수 있다.

- 단순 Roleplay가 길게 이어질 수 있다.
- 질문과 답변만 반복될 수 있다.
- 사용자가 점차 개인적인 이야기를 꺼내고 캐릭터와의 관계를 명시적으로 다루는 대화일 수 있다.

따라서 본 프로젝트의 핵심 질문은 다음과 같다.

> **대화를 오래 지속시키는 상호작용과 관계 형성을 만드는 상호작용은 같은가?**

## 3. Research Questions
1. 어떤 AI 응답 이후 사용자의 대화가 더 오래 지속되는가?
2. 대화 초반과 후반의 사용자 행동은 어떻게 달라지는가?
3. 짧은 대화와 긴 대화는 어떤 구조적 차이를 보이는가?
4. 캐릭터별로 대화 지속 패턴에 차이가 있는가?
5. 대화 지속성과 관계적 상호작용은 함께 증가하는가, 아니면 별개로 움직이는가?

## 4. 분석 단위
기본 분석 단위는 **Conversation**과 **Turn**이다.

| 분석 단위 | 예시 변수 |
| --- | --- |
| Conversation | conversation_id, character_id/name, total_turns |
| Turn | turn_number, speaker, message, message_length |
| Continuation | next_turn 여부, remaining_turns, 이후 5/10턴 지속 여부 |
| Progression | 초반/중반/후반 또는 turn percentile |

관계성 스코어링 기준, 세부 라벨 정의, 가중치는 분석자가 직접 설계한다. 본 기획서에서는 해당 기준을 사전에 확정하지 않는다.

## 5. 사용할 데이터

### 5.1 Primary Dataset — PIPPA
PIPPA는 Character.AI 사용자들이 자발적으로 제공한 실제 대화 로그를 모은 공개 데이터셋이다. 약 26,000개 conversation과 100만 줄 이상의 dialogue를 포함하고, 1,000개 이상의 캐릭터 persona가 포함된다.

대화 전체 sequence와 human/AI 발화 구분이 가능해 turn-level 분석에 적합하다.

- 활용 목적: conversation depth, turn continuation, character별 차이 분석
- 장점: 충분한 규모, 실제 Character.AI 대화, 대화 sequence 보존
- 한계: 2023년 데이터, 자발적 제출 데이터, NSFW/민감 콘텐츠가 일부 포함될 수 있음
- Source: https://huggingface.co/datasets/PygmalionAI/PIPPA

### 5.2 Validation Dataset — RP-Opus
RP-Opus는 2026년 공개된 AI emotional companion/roleplay 대화 데이터셋이다. 대화당 4~60턴, user/assistant message sequence, 캐릭터명, 생성일시 등을 제공하며 한국어를 포함한 다국어 데이터가 있다.

- 활용 목적: PIPPA에서 발견한 패턴이 최근 데이터에서도 나타나는지 확인
- 장점: 2026년 데이터, multi-turn, 한국어 포함
- 한계: gated access, CC BY-NC 4.0, 개인 연구/포트폴리오 용도 중심
- Source: https://huggingface.co/datasets/taozi555/rp-opus

## 6. 분석 방향

### Phase 1 — Data Structure & EDA
- conversation 길이 분포
- turn 수 분포
- 사용자/AI 메시지 길이
- 캐릭터별 conversation 수
- short vs long conversation 구조 비교

### Phase 2 — Turn-level Product Analysis
각 AI 응답 이후:

- 사용자가 다음 턴을 이어가는지
- 이후 몇 턴이 더 지속되는지
- 사용자 메시지 길이와 참여 강도가 어떻게 변하는지

를 분석한다.

### Phase 3 — Conversation Progression
대화를 초반/중반/후반 또는 turn percentile로 나눠 interaction pattern이 시간에 따라 어떻게 달라지는지 본다.

### Phase 4 — Relationship Analysis
분석자가 직접 정의한 관계성 기준을 적용해 대화 지속성과 관계 형성이 동일한 현상인지, 서로 다른 축인지 확인한다.

## 7. 분석 방법 후보
방법론을 먼저 정하고 데이터를 끼워 맞추지 않는다. EDA 이후 연구 질문에 필요한 수준으로 선택한다.

- SQL / Python을 활용한 conversation-turn mart 생성
- 분포 비교 및 통계 검정
- turn-level continuation / survival analysis
- conversation progression 분석
- 필요 시 clustering 또는 sequence analysis
- 시각화: turn depth, continuation curve, character별 패턴, progression chart

## 8. 20일 실행 계획

| 기간 | 작업 |
| --- | --- |
| Day 1–2 | PIPPA / RP-Opus 데이터 구조 확인, 샘플링, 분석 범위 확정 |
| Day 3–5 | 전처리 및 Conversation-Turn mart 생성 |
| Day 6–8 | EDA: 길이·턴·캐릭터·short/long conversation 분석 |
| Day 9–12 | Turn-level continuation 분석 |
| Day 13–15 | Conversation progression 분석 |
| Day 16–17 | 직접 정의한 관계성 기준 적용 및 추가 분석 |
| Day 18 | Product Insight 및 후속 가설 정리 |
| Day 19 | 시각화 / 대시보드 |
| Day 20 | 포트폴리오 문서화 및 QA |

## 9. 기대 산출물
- Conversation / Turn 분석 데이터마트
- 캐릭터챗의 대화 지속 구조에 대한 EDA
- 어떤 상호작용 이후 대화가 더 지속되는지에 대한 분석
- 대화 진행에 따른 interaction pattern 변화
- 대화 지속성과 관계 형성의 관계에 대한 해석
- 캐릭터챗 Product Hypothesis 및 UX 제안

## 10. Product 관점의 최종 질문
> **캐릭터챗에서 사용자를 오래 머물게 하는 것은 단순히 ‘재미있는 대답’인가, 아니면 ‘관계가 이어지고 있다고 느끼게 하는 경험’인가?**

분석 결과는 Memory, Personalization, Character Consistency, Conversation Design, Relationship Continuity와 같은 기능 가설로 연결한다.

## 11. 후속 분석 — Immersion vs Relationship
캐릭터챗 분석 이후에는 스토리챗과 비교하는 후속 프로젝트로 확장한다.

캐릭터챗이 **관계의 연속성**으로 지속 사용을 만든다면, 스토리챗은 **다음 전개에 대한 몰입과 선택의 연속성**으로 지속 사용을 만들 수 있다.

| 축 | 캐릭터챗 | 스토리챗 |
| --- | --- | --- |
| 핵심 경험 | 관계 / 상호작용 지속 | 서사 / 다음 전개 몰입 |
| 행동 단위 | Conversation Turn | Decision Event / Story Progression |
| 주요 공개 데이터 | PIPPA, RP-Opus | Rushes |
| 핵심 질문 | 왜 계속 대화하는가? | 왜 다음 장면으로 넘어가는가? |
| 후속 비즈니스 질문 | 관계 기반 engagement가 유료 전환으로 이어지는가? | 몰입 기반 engagement가 유료 전환으로 이어지는가? |

Microsoft Research의 Rushes는 2026년 공개된 interactive narrative 데이터셋으로, 8,167명의 사용자와 44,226개 decision event, 6개 게임에서 time-ordered user trajectory를 제공한다.

- Source: https://www.microsoft.com/en-us/research/publication/rushes-a-human-preference-dataset-for-pluralistic-alignment/

공개 데이터에는 실제 결제 로그가 없으므로 이번 단계에서는 과금 우열을 직접 검증하지 않는다. 대신 Relationship 기반 engagement와 Immersion 기반 engagement의 구조를 비교하고, 향후 결제 데이터가 확보될 경우 유료 전환·구독 지속으로 확장한다.

## 12. 프로젝트 범위 원칙
- 20일 내 완성을 우선하며, 메인 데이터는 PIPPA로 고정한다.
- RP-Opus는 검증용이며, 접근 또는 전처리 비용이 크면 제외한다.
- 관계성 스코어의 기준·가중치는 분석자가 직접 정의한다.
- 결제 데이터가 없으므로 과금 효과를 직접 입증했다고 주장하지 않는다.
- 후속 스토리챗 비교는 별도 프로젝트 또는 확장 분석으로 분리한다.
- 오픈소스 캐릭터챗 분석은 제품·기술 구조 이해를 목적으로 하며, 완성형 캐릭터챗 구현은 본 프로젝트 범위에 포함하지 않는다.
- 필요 시 핵심 기능 1개에 한해 Prototype 또는 Eval 실험으로 확장한다.

## 13. AI Product Understanding — 오픈소스 캐릭터챗 구조 분석

### 13.1 목적
완성형 캐릭터챗을 직접 개발하는 것이 아니라, 공개된 오픈소스 프로젝트를 통해 **캐릭터챗의 실제 제품·기술 구조를 이해하고 데이터 분석 결과를 구현 가능한 Product Hypothesis로 연결하는 것**을 목표로 한다.

데이터 분석이 “어떤 상호작용이 대화를 지속시키는가”를 밝히는 단계라면, 본 트랙은 “그 상호작용을 제품에서는 어떤 구조로 구현할 수 있는가”를 이해하는 단계다.

### 13.2 분석 대상 후보
- **RisuAI** — Persona / Lorebook / Memory / Prompt 구조
- **SillyTavern** — Character Card / Context / Memory 확장 구조
- **a16z Companion App** — Retrieval + Memory 기반 최소 Companion 구조
- **OpenPersona** — Persona / Memory / Voice 구조 참고

### 13.3 확인할 질문
1. Character Persona는 어떻게 정의되고 LLM 입력에 주입되는가?
2. Conversation Context는 어떤 방식으로 유지되는가?
3. 장기 Memory는 무엇을 저장하고, 언제 retrieval하는가?
4. Persona Consistency는 어떤 구조로 유지되는가?
5. Context Window 한계는 어떻게 처리하는가?
6. Prompt는 어떤 구성 요소로 조립되는가?
7. 품질·Latency·Cost 사이에는 어떤 trade-off가 있는가?
8. 데이터 분석에서 발견한 interaction pattern을 실제 기능으로 구현하려면 어떤 기술 메커니즘이 필요한가?

### 13.4 Product 연결 프레임
분석 결과를 아래 구조로 연결한다.

> **Data Finding → Product Problem → Technical Mechanism → Feature Hypothesis**

예시:

> 과거 맥락을 이어받는 응답 이후 conversation continuation이 높다
> → 관계 연속성이 engagement에 영향을 줄 가능성
> → Memory Retrieval / Context Injection 구조 확인
> → Relationship Memory 기능 가설
> → 향후 Eval 또는 Prototype 실험 후보

### 13.5 산출물
- 캐릭터챗 핵심 시스템 구조도
- Persona / Prompt / Context / Memory / Retrieval 구성요소 정리
- 오픈소스 프로젝트별 구현 접근 비교
- 데이터 분석 결과와 기술 메커니즘의 연결표
- Memory / Personalization / Character Consistency 중 우선 검증할 Product Hypothesis 도출

### 13.6 확장 원칙
본 트랙의 목적은 기술 스택 자체를 깊게 구현하는 것이 아니라, AI Product Manager 관점에서 기능이 어떤 구조와 제약 위에서 동작하는지 이해하는 것이다.

따라서 전체 캐릭터챗 구현은 하지 않으며, 분석 결과상 가장 중요한 기능이 명확해질 경우에만 해당 기능 1개에 대해 Prototype 또는 Eval을 수행한다.
