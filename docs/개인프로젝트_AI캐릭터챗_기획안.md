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

핵심 목표는 완성형 캐릭터챗 서비스를 만드는 것이 아니라, **공개 데이터 분석에서 출발해 실제 AI Product 의사결정까지 이어지는 과정을 보여주는 것**이다.

---

## 2. 핵심 문제 정의
AI 캐릭터챗에서 단순히 대화가 길다는 사실만으로 좋은 경험이라고 말할 수는 없다.

같은 30턴의 대화라도:

- 단순 Roleplay가 반복될 수 있다.
- 질문과 답변만 기계적으로 이어질 수 있다.
- 사용자가 점차 개인적인 이야기를 꺼낼 수 있다.
- 캐릭터가 이전 대화를 참조하며 관계가 이어지는 느낌을 줄 수 있다.
- 내용은 맞지만 번역체·AI 말투 때문에 캐릭터가 인간처럼 느껴지지 않을 수 있다.

따라서 메인 데이터 분석에서는 **현재 공개 데이터가 실제로 답할 수 있는 범위**만 다룬다.

> **긴 대화와 짧은 대화는 어떤 interaction 구조 차이를 보이는가?**

> **대화가 진행되면서 관계적 interaction은 어떻게 변화하는가?**

> **특정 AI 응답 패턴 이후 conversation continuation은 어떻게 달라지는가?**

Retention, 기능 효과, 인과관계는 공개 로그만으로 직접 주장하지 않고 별도 실험으로 분리한다.

---

## 3. Main Research Questions — Dataset Answerable

### Q1. 긴 대화와 짧은 대화는 어떤 차이가 있는가?
긴 conversation과 짧은 conversation을 비교해, 대화 초반부터 나타나는 구조적 차이와 진행 중 변화 패턴을 확인한다.

분석 후보:
- 사용자 / AI 메시지 길이
- 질문 빈도
- 사용자 자기노출
- 감정 표현
- 개인 취향 공유
- 관계적 표현
- 캐릭터별 차이

핵심 질문:

> **대화가 오래 이어지는 conversation은 처음부터 다른가, 아니면 대화가 진행되면서 달라지는가?**

### Q2. 대화가 진행되면서 관계적 interaction은 어떻게 변화하는가?
Conversation을 초반 / 중반 / 후반 또는 turn percentile로 나누고 관계적 상호작용의 변화 패턴을 본다.

관찰 후보:

> 가벼운 대화 → 취향 공유 → 자기노출 → 감정 표현 → 관계 언급 → 과거 맥락 참조 → 향후 상호작용 언급

이와 유사한 progression이 실제 데이터에서 나타나는지 확인한다.

단, 이를 “실제 관계가 형성되었다”고 해석하지 않고 **관계적 interaction pattern이 증가·변화한다** 수준으로 표현한다.

### Q3. 특정 AI 응답 이후 conversation continuation은 어떻게 달라지는가?
AI 응답의 특성에 따라 사용자가 이후 대화를 얼마나 더 이어가는지 확인한다.

분석 후보:
- 질문을 포함한 응답
- 감정에 반응한 응답
- 사용자 정보를 반영한 응답
- 이전 맥락을 참조한 응답
- 캐릭터 persona와 일관된 응답

관찰 지표:
- next turn 여부
- 이후 남은 turn 수
- 이후 5 turn 지속 여부
- 이후 10 turn 지속 여부
- 사용자 메시지 길이 변화

이 단계에서는 **인과관계가 아니라 association**만 분석한다.

---

## 4. Sub Questions / Hypothesis Candidates
메인 질문을 풀기 위해 아래 세부 질문을 가설 후보로 사용한다.

예시:
- 과거 맥락을 참조하는 AI 응답 이후 conversation continuation이 더 높은가?
- 대화 후반으로 갈수록 self-disclosure 비율이 증가하는가?
- 관계적 표현이 많은 conversation은 단순히 긴 conversation과 동일한 집단인가?
- 특정 캐릭터 / persona 유형에서 continuation pattern이 다르게 나타나는가?
- 감정 반영 응답 이후 사용자의 메시지 길이나 이후 turn 수가 달라지는가?

이 가설들은 EDA 이후 실제 데이터 구조와 분포를 보고 추가·삭제한다.

---

## 5. 분석 단위
기본 분석 단위는 **Conversation**과 **Turn**이다.

| 분석 단위 | 예시 변수 |
| --- | --- |
| Conversation | conversation_id, character_id/name, total_turns |
| Turn | turn_number, speaker, message, message_length |
| Continuation | next_turn 여부, remaining_turns, 이후 5/10턴 지속 여부 |
| Progression | 초반/중반/후반 또는 turn percentile |
| Interaction | 질문, 자기노출, 감정표현, 과거 맥락 참조 등 |
| Relationship | 관계 표현, 관계 호칭, 향후 상호작용 언급 등 |

관계성은 EDA 전에 임의의 단일 점수로 고정하지 않는다. 먼저 interaction taxonomy를 정의하고 각 패턴의 분포와 progression을 본다.

---

## 6. 사용할 데이터

### 6.1 Primary Dataset — PIPPA
PIPPA는 Character.AI 사용자들이 자발적으로 제공한 실제 대화 로그를 모은 공개 데이터셋이다.

주요 활용:
- Conversation depth
- Turn-level continuation
- Short vs Long conversation 비교
- Conversation progression
- Character별 차이
- Relationship interaction pattern

한계:
- 한 conversation 내부 sequence는 볼 수 있지만 동일 사용자의 D1 / D7 재방문은 추적할 수 없다.
- 따라서 conversation continuation과 retention을 동일하게 해석하지 않는다.
- 자발적 제출 데이터이므로 selection bias가 존재할 수 있다.
- NSFW / 민감 콘텐츠가 포함될 수 있다.

Source: https://huggingface.co/datasets/PygmalionAI/PIPPA

### 6.2 Validation Dataset — RP-Opus
최근 AI emotional companion / roleplay 대화 데이터셋으로, PIPPA 분석에서 발견한 패턴의 재현 가능성 또는 한국어 conversation 탐색에 활용한다.

활용 후보:
- 최근 multi-turn interaction pattern 검증
- 한국어 subset 탐색
- Character Voice / 자연스러움 평가 후보

접근 또는 전처리 비용이 크면 메인 프로젝트에서는 제외한다.

Source: https://huggingface.co/datasets/taozi555/rp-opus

### 6.3 Optional Eval Set — Korean Character Dialogue
한국어 자연스러움이나 Character Voice 문제를 직접 검증할 필요가 생기면 소규모 Eval Set을 별도로 만든다.

평가 후보:
- 자연스러운 한국어 구어체
- 번역체 / 직역투 여부
- 캐릭터 고유 말투 유지
- Persona Consistency
- 이전 맥락 Recall
- 과도한 설명체 / AI 어투
- 관계 단계에 맞는 반응

이 Eval Set은 메인 로그 분석과 분리한다.

---

## 7. 데이터 분석 방향

### Phase 1 — Data Structure & EDA
- conversation 길이 분포
- turn 수 분포
- 사용자 / AI 메시지 길이
- 캐릭터별 conversation 수
- short vs long conversation 구조 비교
- 민감 콘텐츠 및 분석 제외 기준 확인

### Phase 2 — Short vs Long Conversation
긴 conversation과 짧은 conversation의 초반·중반·후반 구조를 비교한다.

확인 후보:
- 초반 5~10턴의 차이
- 사용자 참여 강도
- 질문 / 감정표현 / 자기노출 빈도
- 캐릭터별 variation

### Phase 3 — Turn-level Continuation
각 AI 응답 이후:
- 사용자가 다음 턴을 이어가는지
- 이후 몇 턴이 더 지속되는지
- 이후 5/10턴까지 이어지는지
- 사용자 메시지 길이가 어떻게 변하는지

를 본다.

### Phase 4 — Conversation Progression / Relationship Interaction
대화를 초반 / 중반 / 후반으로 나눠 interaction pattern이 시간에 따라 어떻게 달라지는지 확인한다.

초기 taxonomy 후보:
- self-disclosure
- emotional expression
- relational language
- personal preference sharing
- past-context reference
- nickname / relationship naming
- future interaction reference

### Phase 5 — Product Translation
분석 결과를 다음 프레임으로 연결한다.

> **Data Finding → Product Problem → Technical Mechanism → Feature Hypothesis**

예시:

> 과거 맥락 참조 interaction에서 더 긴 continuation이 관찰됨
> → 관계의 연속성이 제품 가치일 가능성
> → Memory Retrieval / Context Injection 구조 검토
> → Relationship Memory Feature Hypothesis

---

## 8. 분석 방법 후보
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

## 9. 데이터로 직접 알 수 없는 것
PIPPA만으로는 다음을 직접 검증할 수 없다.

- D1 / D3 / D7 Retention
- 동일 사용자의 서비스 재방문
- 특정 기능이 retention을 증가시켰는지 여부
- Memory / Persona / Character Voice가 행동을 변화시켰다는 인과관계
- 실제 결제 전환 또는 구독 유지 효과

따라서:

> **Conversation Continuation ≠ Retention**

으로 명확히 구분한다.

공개 데이터 분석에서는 “어떤 패턴과 더 긴 conversation이 함께 나타났다” 수준까지 말하고, 그 다음 단계는 Product Hypothesis 또는 별도 실험으로 연결한다.

---

## 10. AI Product Understanding — 오픈소스 캐릭터챗 구조 분석

### 10.1 목적
공개 오픈소스 프로젝트를 통해 **캐릭터챗의 실제 제품·기술 구조를 이해하고 데이터 분석 결과를 구현 가능한 Product Hypothesis로 연결한다.**

### 10.2 분석 대상 후보
- **RisuAI** — Persona / Lorebook / Memory / Prompt 구조
- **SillyTavern** — Character Card / Context / Memory 구조
- **a16z Companion App** — Retrieval + Memory 기반 Companion 구조
- **OpenPersona** — Persona / Memory / Voice 구조 참고

모든 프로젝트를 동일한 깊이로 분석하지 않는다. 1~2개를 메인으로 보고 나머지는 비교 참고용으로 사용한다.

### 10.3 확인할 질문
1. Character Persona는 어떻게 정의되고 LLM 입력에 주입되는가?
2. Conversation Context는 어떤 방식으로 유지되는가?
3. 장기 Memory는 무엇을 저장하고 언제 retrieval하는가?
4. Persona Consistency는 어떤 구조로 유지되는가?
5. Context Window 한계는 어떻게 처리하는가?
6. Prompt는 어떤 구성 요소로 조립되는가?
7. Character Voice를 유지하기 위해 어떤 제어가 가능한가?
8. 품질·Latency·Cost 사이에는 어떤 trade-off가 있는가?
9. 데이터 분석에서 발견한 interaction pattern을 실제 기능으로 구현하려면 어떤 기술 메커니즘이 필요한가?

### 10.4 산출물
- 캐릭터챗 핵심 시스템 구조도
- Persona / Prompt / Context / Memory / Retrieval 구성요소 정리
- 오픈소스 프로젝트별 구현 접근 비교
- Data Finding ↔ Technical Mechanism 연결표
- 우선 검증할 Product Hypothesis 도출

---

## 11. Prototype / Eval — 핵심 기능 1개
메인 분석 결과에서 명확한 Product Problem이 발견된 경우에만 수행한다.

후보:
- Relationship Memory
- Character Voice / Natural Korean
- Persona Consistency
- Context Recall

실험 구조:

> **Problem Definition → Success / Failure Criteria → Test Set → Baseline vs Variant → Failure Analysis → Product Decision**

예: Character Voice를 선택한 경우

### Baseline
기본적인 Character Persona Prompt

### Variant
- 한국어 구어체 규칙
- Character-specific 말투
- Few-shot dialogue examples
- 번역체 방지 지침

### Eval
- 한국어 자연스러움
- 번역체 여부
- 캐릭터성
- Persona Consistency
- 문맥 적합성
- 인간다운 응답
- 다시 대화하고 싶은 정도

완성형 서비스를 만드는 것이 아니라 **검증 가능한 실험 환경을 만드는 것**이 목적이다.

---

## 12. User Experiment / Retention Track
실제 retention을 검증하려면 별도 사용자 실험이 필요하다.

가능할 경우:

> **Day 0 첫 대화 → D1 재방문 → 필요 시 D3 / D7**

비교 후보:

> Baseline Character vs Memory / Character Voice 개선 Character

측정 후보:
- Session length
- Conversation turns
- D1 return
- D3 / D7 return
- 다시 대화할 의향
- 캐릭터 선호 / 애착 관련 평가

사용자 수가 충분하지 않을 경우 retention을 일반화하지 않고 **exploratory experiment**로 표현한다.

---

## 13. 한국어 Character Voice / Natural Language Quality
별도의 중요한 Product Quality 축으로 둔다.

핵심 문제:

> **문법적으로 틀리지는 않지만 번역체·설명체·AI 말투 때문에 인간이나 캐릭터처럼 느껴지지 않는 문제**

평가 후보:
- 직역투
- 과도한 완전문
- 부자연스러운 대명사 사용
- 한국인이 잘 쓰지 않는 표현
- 과도한 설명
- 모든 캐릭터가 비슷한 말투를 사용하는 문제
- 설정과 다른 존댓말 / 반말
- 감정 상황과 어울리지 않는 문장 길이

이 문제는 PIPPA 메인 분석과 분리해 **한국어 Eval Track**으로 둔다.

---

## 14. 스토리챗과의 차이
스토리챗은 이번 프로젝트의 메인이 아니다.

| Character / Companion | Story Chat |
| --- | --- |
| 관계 지속 | 서사 몰입 |
| 왜 다시 말하고 싶은가 | 왜 다음 장면을 보고 싶은가 |
| Memory | Narrative |
| Persona | World Building |
| Character Voice | Plot / Pacing |
| Relationship Continuity | Story Progression |

Story Chat 분석은 필요할 경우 후속 프로젝트로 둔다.

---

## 15. 20일 실행 계획

| 기간 | 작업 |
| --- | --- |
| Day 1–2 | PIPPA 구조 확인, 샘플링, 제외 기준 및 분석 범위 확정 |
| Day 3–5 | 전처리 및 Conversation-Turn Mart 생성 |
| Day 6–8 | EDA + Short vs Long Conversation 분석 |
| Day 9–11 | Turn-level continuation 분석 |
| Day 12–13 | Conversation progression 분석 |
| Day 14–15 | Relationship interaction taxonomy 및 분석 |
| Day 16 | 오픈소스 캐릭터챗 구조 분석 |
| Day 17 | Data Finding → Product Hypothesis 연결 |
| Day 18 | 핵심 가설 1개 Eval 설계 또는 추가 분석 |
| Day 19 | 시각화 / 구조도 / 결과 정리 |
| Day 20 | 포트폴리오 문서화 및 QA |

※ **20일 내 Main Data Analysis 완성**을 최우선으로 한다. Prototype / Eval / User Experiment는 분석 결과와 리소스에 따라 후속 단계로 분리할 수 있다.

---

## 16. 기대 산출물

### Data Analysis
- Conversation / Turn 분석 데이터마트
- Short vs Long Conversation 비교
- Turn-level continuation analysis
- Conversation progression analysis
- 관계적 interaction pattern 분석

### AI Product Understanding
- 캐릭터챗 시스템 구조도
- Persona / Context / Memory / Retrieval 분석
- 오픈소스 구조 비교

### Product Output
- Product Insight
- Product Problem 1개 이상
- Feature Hypothesis
- 가능하면 Eval Framework / Prototype 결과
- 포트폴리오 Case Study

### Optional Experiment
- Baseline vs Variant 결과
- 가능하면 Session Continuation 또는 D1 Retention 탐색

---

## 17. 프로젝트 범위 원칙
- 메인 제품 범주는 **Character / Companion**으로 고정한다.
- 메인 분석은 **현재 데이터셋으로 실제 답할 수 있는 질문만** 다룬다.
- Conversation Continuation과 Retention을 구분한다.
- 관찰 데이터에서 인과관계를 주장하지 않는다.
- 메인 데이터는 PIPPA로 고정한다.
- RP-Opus는 Validation 또는 한국어 품질 탐색용이며, 접근·전처리 비용이 크면 제외한다.
- 결제 데이터가 없으므로 과금 효과를 직접 입증하지 않는다.
- Monetization은 Product Hypothesis 수준에서만 연결한다.
- Prototype / Eval은 핵심 문제 1개가 명확해질 때만 수행한다.
- User Experiment는 별도 후속 단계로 분리할 수 있다.
- Story Chat 분석은 별도 후속 프로젝트로 둔다.
- NSFW / 민감 콘텐츠는 분석 목적에 필요하지 않으면 제외하거나 별도 처리한다.

---

## 18. 프로젝트 독립성 및 출처 원칙
본 프로젝트는 **공개 데이터셋, 공개 오픈소스, 공개 문헌만 사용해 독립적으로 수행한다.**

이전 근무지의 내부 데이터, 비공개 기획 문서, 프롬프트, KPI, 정책, 코드 또는 기타 confidential information은 사용하지 않는다.

프로젝트의 분석 질문과 Product Hypothesis는 공개 자료와 본 프로젝트에서 직접 수행한 분석 결과를 기반으로 도출한다.

---

## 19. 프로젝트 완료 기준
이 프로젝트는 아래 조건을 충족하면 1차 완료로 본다.

1. 재현 가능한 Conversation-Turn Mart가 있다.
2. 긴 대화와 짧은 대화의 차이를 최소 1개 이상 설명할 수 있다.
3. Conversation progression에 따른 interaction pattern 변화를 설명할 수 있다.
4. Turn-level continuation과 관련된 pattern을 최소 1개 이상 제시한다.
5. 관찰 결과와 인과적 해석을 명확히 구분한다.
6. Conversation Continuation과 Retention을 구분한다.
7. 분석 결과를 최소 1개의 Product Problem / Feature Hypothesis로 번역한다.
8. 해당 Problem이 실제 캐릭터챗 구조에서 어떤 Mechanism과 연결되는지 설명한다.
9. 최종 Case Study에서 **문제 정의 → 분석 → 해석 → Product Decision** 흐름이 보인다.

이 기준을 충족한 뒤에만 Prototype / Eval / User Experiment / Story Chat 비교로 확장한다.
