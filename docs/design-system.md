# Luna UI Design System

이 문서는 Luna Memory의 프론트엔드 UI를 확장할 때 사용하는 **단일 디자인 기준**입니다.

새 UI를 추가할 때는 기존 `styles.css`의 색상, 간격, 라운드, 타이포그래피, 상태 표현을 우선 재사용합니다. 특별한 이유 없이 새로운 색상·그림자·폰트 크기·버튼 스타일을 만들지 않습니다.

---

## 1. 디자인 방향

Luna의 UI는 다음 인상을 유지합니다.

- 부드럽고 차분한 개인형 AI companion
- 밝은 뉴트럴 배경 + 보라색 포인트
- 정보 밀도는 낮게, 운영/디버깅 정보는 작고 정돈되게
- 캐릭터챗이 중심이고 설정/메모리는 보조 영역
- 새 기능이 추가되어도 기존 채팅 화면보다 시각적으로 튀지 않게 한다

우선순위는 다음과 같습니다.

1. 대화 가독성
2. 현재 상태 파악
3. 설정과 디버깅 편의성
4. 장식

---

## 2. 컬러 토큰

현재 `:root` 토큰을 디자인 시스템의 기본 색상으로 사용합니다.

| Token | Value | 용도 |
|---|---|---|
| `--ink` | `#282c3a` | 기본 텍스트, 강한 버튼 |
| `--muted` | `#818697` | 보조 텍스트, 설명 |
| `--line` | `#e9e8ee` | 구분선, 약한 border |
| `--paper` | `#fbfaf8` | 앱 바탕 |
| `--panel` | `#f5f2ee` | 보조 패널 배경 |
| `--accent` | `#7657d6` | 핵심 액션, 사용자 메시지 |
| `--accent-dark` | `#6042bc` | hover, 강조 텍스트 |
| `--accent-soft` | `#eee9fb` | 약한 강조 배경 |
| `--green` | `#4eb48a` | 성공/연결 상태 |

### 상태 색상 원칙

- 성공/정상: `--green`
- 주요 액션: `--accent`
- 약한 강조: `--accent-soft`
- 오류: 기존 `#c3535b` / `#d76f73` 계열 사용
- 비활성/중립: `--muted`, `--line`

**금지:** 새 기능 하나 때문에 임의의 파랑, 주황, 네온 컬러를 추가하지 않는다.

---

## 3. 타이포그래피

기본 폰트:

```css
font-family: "DM Sans", "Noto Sans KR", sans-serif;
```

권장 크기 체계:

| 크기 | 용도 |
|---:|---|
| 20–21px | 브랜드/강한 타이틀 |
| 16–18px | 패널/화면 제목 |
| 13px | 채팅 본문 |
| 11–12px | 설정, 폼 라벨, 패널 설명 |
| 9–10px | 메타 정보, 시간, 상태 보조문구 |

원칙:

- 본문은 13px 전후를 유지한다.
- 새 설정 UI는 11–12px을 기본으로 한다.
- 중요하지 않은 정보는 크기를 키우기보다 색을 `--muted`로 낮춘다.
- 한 화면에서 새로운 폰트 크기 단계를 임의로 추가하지 않는다.

---

## 4. 간격 체계

현재 UI는 4px 배수에 가까운 간격을 중심으로 사용합니다.

권장 spacing:

- 4px: 아주 작은 보정
- 8px: 컨트롤 내부/라벨 간격
- 10–12px: 작은 컴포넌트 padding
- 14–16px: 카드/입력 주요 padding
- 20–24px: 섹션 간 간격
- 28–30px: 주요 패널 바깥 padding

새 컴포넌트는 먼저 **8 / 12 / 16 / 24px** 중 하나로 맞춥니다.

---

## 5. Radius

현재 화면의 기본 radius 체계:

| Radius | 용도 |
|---:|---|
| 8–10px | 버튼, 작은 입력, 상태 UI |
| 12–14px | 카드, 채팅 입력, 메시지 |
| 15–18px | 아바타, 다이얼로그, 큰 카드 |

새 UI는 기본적으로:

- 버튼: 9–10px
- 입력: 10px
- 카드: 12px
- 큰 modal/card: 18px

을 사용합니다.

---

## 6. Elevation / Shadow

그림자는 매우 약하게 사용합니다.

기존 예시:

```css
box-shadow: 0 8px 28px #39304f0a;
box-shadow: 0 5px 18px #41364c08;
box-shadow: 0 20px 60px #211b4426;
```

원칙:

- 일반 카드: 거의 평면
- 입력 focus / floating panel / dialog에만 shadow
- 새 기능을 강조하기 위해 강한 shadow를 추가하지 않는다

---

## 7. 레이아웃

Desktop 기본 구조:

```text
[ Left Sidebar 270px ]
[ Main Chat flexible ]
[ Memory Panel 310px ]
```

현재 기준:

```css
.shell {
  grid-template-columns: 270px minmax(440px, 1fr) 310px;
}
```

Responsive:

- 980px 이하: memory panel을 overlay drawer로 전환
- 700px 이하: sidebar 숨김, chat 중심 모바일 레이아웃

새 UI는 메인 채팅 영역을 침범하기 전에 sidebar / memory panel / dialog / toast 중 적절한 위치를 먼저 고려합니다.

---

## 8. Form controls

입력창은 기존 스타일을 재사용합니다.

기본 규칙:

- border: 연한 회색
- radius: 10px
- background: 거의 흰색
- focus: 보라색 border + 매우 약한 focus ring
- placeholder/설명: `--muted`

새 입력 UI는 별도 스타일을 만들기보다 기존 `textarea`, `input`, `.input-row` 패턴을 확장합니다.

---

## 9. Buttons

### Primary
사용자 행동의 핵심 한 개만 강한 색을 사용합니다.

예:
- 보내기
- 주요 입장/확정 액션

색상:
- background: `--accent`
- hover: `--accent-dark`

### Secondary
설정 저장, 평가, 다시 시도 등은 soft 스타일을 사용합니다.

예:
```css
border: 1px solid #d8d2f4;
background: #f7f5ff;
color: var(--accent-dark);
```

원칙:

- 한 영역에 강한 primary 버튼을 여러 개 두지 않는다.
- 새 버튼 스타일이 필요하면 primary / secondary / text 중 하나에 먼저 매핑한다.

---

## 10. Chat bubble

Assistant:
- background: `#f2f0f5`
- text: `--ink`
- left aligned
- avatar 표시

User:
- background: `--accent`
- text: white
- right aligned

원칙:

- 시스템 상태/오류를 일반 채팅 답변과 동일하게 보이게 하지 않는다.
- 네트워크 오류, 재시도 상태 등은 보조 UI 또는 별도 상태 메시지로 처리한다.
- 캐릭터 응답 스타일은 일관되게 유지한다.

---

## 11. Sidebar / Settings

Sidebar는 운영/테스트 설정이 들어갈 수 있으나 다음을 지킵니다.

- 섹션 제목은 `.eyebrow`
- 라벨은 `.field-label`
- 각 필드 사이 간격은 약 8px
- 텍스트 영역은 기존 `#characterPrompt`, `#systemRules` 패턴을 따른다
- 저장 완료 메시지는 작고 조용하게 표현한다
- 설정 영역이 길어질 경우 sidebar scroll을 사용한다

테스트용 UI라도 메인 채팅보다 강하게 보이지 않게 합니다.

---

## 12. Memory panel

Memory panel은 디버깅/관찰 영역입니다.

- background: `--panel`
- card: white
- border: `#e2dee7`
- score / signal은 작은 텍스트 사용
- 메인 채팅보다 시각적 우선순위를 낮게 유지

새 메모리 정보는 카드 구조를 확장하되 별도 대시보드 스타일을 만들지 않습니다.

---

## 13. Status / Toast / Dialog

### Status
작은 dot + 짧은 텍스트 조합 사용.

### Toast
- 일시적인 성공/저장 메시지
- 화면 하단 중앙
- dark background
- 약 2초 노출

### Dialog
평가, 중요 확인 등 화면 맥락을 잠깐 끊어도 되는 경우 사용.

원칙:
- 단순 설정은 dialog를 만들지 않는다.
- 저장 성공은 dialog 대신 toast.
- 실패/재시도는 사용자가 다음 행동을 바로 할 수 있게 한다.

---

## 14. Motion

현재 motion은 매우 약합니다.

- message arrive: 약 0.28s
- drawer: 약 0.25s
- toast: 약 0.2s

새 animation은 보통 0.15–0.3s 범위로 제한합니다.

**금지:** bounce, 강한 scale, 반복 flashing, 과한 spring animation.

---

## 15. 접근성

새 UI 추가 시 최소 기준:

- 입력에는 반드시 `label` 연결
- 아이콘-only 버튼은 `aria-label`
- 상태 텍스트는 필요한 경우 `aria-live`
- 색상만으로 성공/실패를 구분하지 않는다
- 클릭 가능한 요소는 `button` 또는 의미에 맞는 semantic element 사용
- 키보드 focus를 제거하지 않는다

---

## 16. 신규 컴포넌트 추가 순서

새 UI를 만들기 전에 아래 순서로 결정합니다.

1. 기존 컴포넌트로 표현 가능한가?
2. 기존 색상 토큰으로 가능한가?
3. 기존 button/input/card 패턴으로 가능한가?
4. sidebar / chat / memory panel / dialog 중 어디에 속하는가?
5. responsive에서 어디로 이동하거나 숨겨질 것인가?

새 CSS selector를 만들더라도 기존 토큰과 패턴을 조합해서 만듭니다.

---

## 17. UI 추가 체크리스트

PR/커밋 전 아래를 확인합니다.

- [ ] 새 색상을 임의로 추가하지 않았는가?
- [ ] 기존 `--accent`, `--muted`, `--line`, `--panel`을 우선 사용했는가?
- [ ] 버튼이 기존 primary/secondary/text 계열 중 하나인가?
- [ ] border-radius가 기존 8–18px 체계 안에 있는가?
- [ ] 폰트 크기가 기존 단계와 맞는가?
- [ ] padding / gap이 기존 8 / 12 / 16 / 24px 계열과 맞는가?
- [ ] 메인 채팅보다 설정 UI가 더 튀지 않는가?
- [ ] 980px / 700px 이하 화면에서 깨지지 않는가?
- [ ] focus / disabled / loading / error 상태가 있는가?
- [ ] root와 `dist/` 정적 파일이 함께 수정되었는가?

---

## 18. 금지 패턴

다음은 특별한 제품 이유가 없는 한 사용하지 않습니다.

- 임의의 gradient 추가
- 새로운 브랜드 컬러 추가
- 지나치게 큰 CTA
- 카드마다 서로 다른 radius
- 기능마다 서로 다른 button 스타일
- inline style 남발
- 정보가 많다는 이유로 font size를 지나치게 줄이는 것
- 디버깅 UI를 메인 캐릭터챗보다 더 강하게 강조하는 것
- desktop에서만 맞고 mobile에서 사라지는 UI
- root 파일만 수정하고 `dist/`를 동기화하지 않는 것

---

## 19. 현재 source of truth

UI 구현의 기준 파일:

- `styles.css`
- `index.html`
- `app.js`

Render static 배포용 동기화 대상:

- `dist/styles.css`
- `dist/index.html`
- `dist/app.js`

새 UI 작업 시 이 문서를 먼저 확인하고, 기존 UI와 다른 스타일이 필요하다면 먼저 이 문서에 새로운 패턴을 정의한 뒤 구현합니다.
