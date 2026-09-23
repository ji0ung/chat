# 캐릭터챗 장기기억 MVP

대화를 임베딩해 사용자별로 저장하고, 새 메시지와 의미가 가까운 기억을 검색한 뒤 캐릭터 시스템 프롬프트에 넣는 최소 예제입니다. 루나와 대화하고 검색된 기억 점수를 확인할 수 있는 반응형 웹 UI도 포함합니다.

상세한 [API 명세](docs/API.md), [어드민·기억 감도 설계](docs/ADMIN.md), [보안 및 입력 Validation 정책](docs/security-input-validation-policy.md), [UI 디자인 시스템](docs/design-system.md)을 함께 제공합니다.

## 화면 실행

백엔드를 실행한 뒤 별도 터미널에서 정적 프론트엔드를 엽니다.

```bash
python3 -m http.server 3000
```

브라우저에서 `http://127.0.0.1:3000`으로 접속합니다. 왼쪽의 **백엔드 API 주소**가 `http://127.0.0.1:8000`인지 확인하고 **연결 저장 및 확인**을 누릅니다.

운영 콘솔은 `http://127.0.0.1:3000/admin.html`에서 확인합니다. 현재 콘솔은 화면과 감도 시뮬레이션을 검증하는 프론트엔드 MVP이며, 저장·발행 버튼은 관리자 API 구현 후 실제 데이터에 연결합니다.

## Vercel에 프론트엔드 배포

이 저장소를 GitHub에 올린 후 Vercel에서 가져오면 별도 빌드 명령 없이 `index.html`을 배포할 수 있습니다. 또는 Vercel CLI가 설정되어 있다면 프로젝트 루트에서 다음을 실행합니다.

```bash
vercel
vercel --prod
```

배포된 화면의 **백엔드 API 주소**에는 외부에서 접근 가능한 HTTPS 백엔드 URL을 입력합니다. 로컬 주소인 `127.0.0.1:8000`은 배포 방문자의 컴퓨터를 가리키므로 사용할 수 없습니다.

백엔드 환경변수 `ALLOWED_ORIGINS`에는 실제 Vercel 주소를 추가합니다.

```dotenv
ALLOWED_ORIGINS=https://your-project.vercel.app,http://localhost:3000,http://127.0.0.1:3000
```

현재 SQLite 백엔드는 로컬 MVP용입니다. 서버리스 환경에서는 파일이 영구 보존되지 않을 수 있으므로 백엔드는 영구 디스크가 있는 서비스에 배포하거나 운영 단계에서 Postgres/pgvector로 교체해야 합니다.

## Render 무료 배포

저장소에 포함된 `render.yaml`을 사용하면 Render Blueprint에서 프론트 화면과 FastAPI API를 함께 만들 수 있습니다.

1. [Render New Blueprint](https://dashboard.render.com/blueprints/new)에서 GitHub의 `ji0ung/chat` 저장소를 선택합니다.
2. `render.yaml`을 확인하고 두 서비스를 생성합니다.
3. API 서비스의 `OPENROUTER_API_KEY`를 입력합니다.
4. 두 서비스가 배포되면 프론트 화면 왼쪽 API 주소에 `https://luna-memory-api.onrender.com` 형태의 실제 API 주소를 입력합니다.

Render 무료 정적 사이트는 화면 확인용으로 적합합니다. FastAPI Web Service는 계정·지역·시점에 따라 결제 수단 등록을 요구할 수 있고, 무료 인스턴스는 일정 시간 요청이 없으면 절전 상태가 됩니다. 현재 Blueprint API는 OpenRouter 무료 모델과 로컬 Sentence Transformers 임베딩을 사용하도록 설정했으며, SQLite는 재시작·재배포 시 데이터가 유지되지 않을 수 있으므로 장기기억 운영 전에는 Postgres/pgvector로 교체해야 합니다.

### 최신 커밋 동기화

Render 서비스의 Settings → Deploy Hook에서 URL을 만든 뒤 GitHub 저장소의 Actions secrets에 `RENDER_DEPLOY_HOOK_URL`로 저장하세요. 이후 `main` 브랜치 push마다 `.github/workflows/render-deploy.yml`이 배포를 요청합니다. 로컬 수동 실행은 다음과 같습니다.

```bash
RENDER_DEPLOY_HOOK_URL='https://api.render.com/deploy/srv-...' ./scripts/render-sync.sh
```

Deploy Hook URL은 비밀번호처럼 취급하고 코드에 직접 커밋하지 않습니다.


## 외부 공유 전 보안 설정

Render 같은 외부 환경에서는 `APP_ENV=production`으로 실행합니다. 이 모드에서는 아래 값이 없거나 안전하지 않으면 서버가 시작되지 않습니다.

```dotenv
APP_ENV=production
APP_ACCESS_TOKEN=16자-이상의-비공개-접근코드
ADMIN_API_TOKEN=충분히-긴-관리자-비밀값
ALLOWED_ORIGINS=https://luna-memory-web.onrender.com
LOG_INCLUDE_CONTENT=false
```

- `APP_ACCESS_TOKEN`: 채팅 입장과 일반 API 호출을 보호하는 하나의 비공개 코드입니다. Render에 설정한 값을 프론트의 액세스 코드 입력창에 그대로 입력합니다.
- `ADMIN_API_TOKEN`: 운영 콘솔에서 사용하는 별도 관리자 비밀값입니다. 일반 사용자에게 공유하지 않습니다.
- 로그 사용자 식별자 해시용 salt는 `ADMIN_API_TOKEN`에서 서버가 내부적으로 파생합니다. 별도 `LOG_HASH_SALT` 설정은 필요하지 않습니다.
- 프론트의 액세스 코드와 관리자 토큰은 `sessionStorage`에만 저장되어 브라우저 탭을 닫으면 사라집니다.
- 실제 서비스 로그인으로 확장할 때는 이 단일 액세스 코드 방식을 JWT/서버 세션으로 교체하세요.

Render Dashboard의 API 서비스 → Environment에서 `APP_ACCESS_TOKEN`과 `ADMIN_API_TOKEN`을 직접 넣습니다. 비밀값은 GitHub에 커밋하지 않습니다.

## 처리 흐름

1. 새 사용자 메시지를 임베딩합니다.
2. 같은 `user_id`의 기억에서 코사인 유사도가 높은 후보를 고릅니다.
3. 후보를 `유사도 60% + 중요도 20% + 최근성 15% + 회상 빈도 5%`로 다시 정렬합니다.
4. 상위 기억을 `<long_term_memory>` 블록으로 캐릭터 프롬프트에 결합합니다.
5. Responses API로 답변을 생성합니다.
6. 사용자 메시지와 캐릭터 답변을 각각 임베딩해 SQLite에 저장합니다.

SQLite가 대화, 벡터, 메타데이터를 한 파일에 보관합니다. 검색량이 커지면 `SQLiteMemoryStore`를 Qdrant, pgvector 또는 Pinecone 구현으로 교체하면 됩니다.

## 실행

Python 3.11 이상을 권장합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env`의 `OPENAI_API_KEY`를 실제 키로 바꾼 뒤 실행합니다.

```bash
uvicorn app.main:app --reload
```

API 문서는 `http://127.0.0.1:8000/docs`에서 확인할 수 있습니다.

## 무료 로컬 실험 모드

공유 대화에서 제안한 무료 실험 방식은 로컬 Ollama를 사용하거나, 임베딩만 로컬 Sentence Transformers로 바꾸는 것입니다. `.env`에서 공급자를 선택합니다.

### Ollama로 임베딩·LLM 모두 실행

Ollama를 설치한 뒤 모델을 한 번만 받습니다.

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

`.env`:

```dotenv
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_CHAT_MODEL=qwen2.5:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

Ollama가 `http://127.0.0.1:11434`에서 실행 중이면 API 비용 없이 반복 대화를 테스트할 수 있습니다.

### 임베딩만 로컬로 실행

```dotenv
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

한국어 품질을 평가할 때는 MiniLM 하나만 믿지 말고 다국어·한국어 임베딩 모델을 비교군으로 추가하세요.

### OpenRouter 무료 모델 비교군

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your-key
OPENROUTER_MODEL=openrouter/free
EMBEDDING_PROVIDER=local
```

무료 모델 목록과 제공량은 바뀔 수 있으므로 장기 운영 비용을 0원으로 가정하지 말고, 로컬 Ollama를 주 실험군으로 두는 편이 안전합니다.

## 사용 예시

첫 대화를 저장합니다.

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user-1",
    "conversation_id": "chat-1",
    "message": "나는 민트초코 아이스크림을 제일 좋아해.",
    "importance": 0.9,
    "character_prompt": "너는 오래된 친구 루나다. 다정하고 장난스럽게 한국어로 답한다."
  }'
```

그 다음 관련 질문을 보내면 이전 기억이 검색됩니다.

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user-1",
    "conversation_id": "chat-2",
    "message": "내가 제일 좋아하는 아이스크림이 뭐였지?",
    "character_prompt": "너는 오래된 친구 루나다. 다정하고 장난스럽게 한국어로 답한다."
  }'
```

응답의 `recalled_memories`에는 디버깅용 검색 결과와 각 랭킹 신호가 포함됩니다. 실제 서비스에서는 이 필드를 사용자에게 숨기는 편이 좋습니다.

## 환경변수

| 이름 | 기본값 | 설명 |
|---|---:|---|
| `OPENAI_API_KEY` | 없음 | OpenAI API 키 |
| `CHAT_MODEL` | `gpt-4.1-mini` | 답변 생성 모델 |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | 임베딩 모델 |
| `MEMORY_DB_PATH` | `data/memories.db` | SQLite 파일 위치 |
| `MEMORY_TOP_K` | `5` | 프롬프트에 넣을 기억 수 |
| `MEMORY_CANDIDATE_LIMIT` | `20` | 의미 유사도 1차 후보 수 |
| `MEMORY_HALF_LIFE_DAYS` | `30` | 최근성 점수가 절반이 되는 기간 |
| `ALLOWED_ORIGINS` | 로컬 프론트 주소 | 브라우저 요청을 허용할 프론트 주소 목록 |
| `LOG_LEVEL` | `INFO` | 애플리케이션 로그 레벨 |
| `LOG_PATH` | `logs/character-memory.jsonl` | JSONL 로그 파일 위치 |
| `LOG_MAX_BYTES` | `10485760` | 파일 하나의 최대 크기(기본 10MB) |
| `LOG_BACKUP_COUNT` | `7` | 회전 후 보관할 이전 로그 수 |
| `LOG_INCLUDE_CONTENT` | `false` | 대화 원문 기록 여부 |
| `LOG_HASH_SALT` | 선택사항 | 미설정 시 `ADMIN_API_TOKEN`에서 자동 파생되는 로그 식별자 해시 salt |

중요도는 API 요청에서 0~1로 지정합니다. MVP에서는 호출자가 직접 부여하지만, 운영 버전에서는 규칙 또는 별도 모델로 선호·약속·관계 변화 같은 사건만 높게 평가하는 것을 권장합니다.

## 데이터·검색 로그

백엔드를 실행하면 `logs/character-memory.jsonl`에 한 줄당 하나의 JSON 이벤트가 기록됩니다. 로그 파일은 기본 10MB 단위로 회전하며 이전 파일 7개를 보관합니다.

주요 이벤트는 다음과 같습니다.

- `chat_received`: 요청 중요도, 메시지 길이와 해시
- `memory_recalled`: 검색 시간, 결과 수, 각 기억의 유사도·중요도·최근성·빈도·종합 점수
- `chat_completed`: 전체 처리 시간, 생성 시간, 답변 길이와 해시
- `http_request_completed`: 경로, 상태 코드, 응답 시간
- `http_request_failed`: 실패한 요청과 예외 정보

모든 이벤트에는 `request_id`가 들어가므로 한 번의 채팅 요청을 연결해서 분석할 수 있습니다. 클라이언트가 `X-Request-ID` 헤더를 보내지 않으면 서버가 UUID를 생성하고 응답 헤더로 돌려줍니다.

기본 설정에서는 대화 원문을 저장하지 않으며 `user_id`와 `conversation_id`도 salt가 적용된 해시로 기록합니다. 운영 환경에서는 `ADMIN_API_TOKEN`에서 안정적인 로그 해시 salt를 자동 파생합니다. 원문이 꼭 필요한 제한된 개발 환경에서만 다음 값을 사용합니다.

```dotenv
LOG_INCLUDE_CONTENT=true
```

원문 로그에는 개인정보가 포함될 수 있으므로 운영 환경에서는 접근 제어, 암호화, 보존 기간 및 사용자 삭제 정책이 추가로 필요합니다.

로그 예시:

```json
{"timestamp":"2026-09-23T10:00:00+00:00","level":"INFO","event":"memory_recalled","request_id":"...","user_ref":"5a02...","duration_ms":18.4,"result_count":2,"results":[{"memory_id":4,"score":0.8123,"similarity":0.88,"importance":0.7,"recency":0.99,"frequency":0.0,"memory_length":18,"memory_sha256":"..."}]}
```

## 테스트

API 키 없이 저장, 사용자 격리, 유사도 검색을 검사할 수 있습니다.

```bash
python -m unittest discover -s tests -v
```

## MVP 이후 권장 개선

- 매 문장을 저장하지 말고 기억 추출/중복 제거 단계를 추가
- 삭제·내보내기·보존 기간 등 개인정보 제어 추가
- 대화 단위 요약과 사실 기억을 분리
- 대규모 데이터에서는 ANN 인덱스를 지원하는 전용 벡터 DB 사용
- 검색 품질 평가셋을 만들어 가중치와 `top_k` 조정

임베딩 생성과 Responses API 호출 형태는 [OpenAI 임베딩 가이드](https://developers.openai.com/api/docs/guides/embeddings) 및 [OpenAI API 빠른 시작](https://developers.openai.com/api/docs/quickstart)을 기준으로 구성했습니다.

## 프로젝트 배경

이 MVP는 AI 캐릭터챗에서 대화 지속과 관계 형성을 만드는 상호작용을 분석하는 개인 데이터 분석 프로젝트의 프로토타입입니다. 핵심 행동 단위는 클릭이나 구매가 아닌 `Conversation Turn`이며, 대화가 진행되면서 관계적 상호작용과 장기기억이 어떻게 나타나는지 탐색합니다.

주요 분석 후보 데이터는 PIPPA(Character.AI 실제 대화 기반 공개 데이터)와 RP-Opus(multi-turn AI companion/roleplay 데이터)입니다. 후속 분석 주제는 Story chat의 몰입과 Character chat의 관계성이 engagement를 만드는 방식의 비교입니다.
