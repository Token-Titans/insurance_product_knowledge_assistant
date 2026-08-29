# InsureAssist — Project Flow (မြန်မာလို)

ဒီ file က project တစ်ခုလုံး ဘယ်လိုအလုပ်လုပ်လဲ ဆိုတာကို မြန်မာလို ရှင်းပြထားတာပါ။ Technical term တွေကို ဘာသာမပြန်ဘဲ အင်္ဂလိပ်လိုပဲ ထားထားပါတယ်။ တိကျတဲ့ spec လိုချင်ရင် `docs/` အောက်မှာရှိတဲ့ မူရင်း document တွေကို ကြည့်ပါ။

---

## ၁။ ဒီ product က ဘာလုပ်တာလဲ

InsureAssist က **insurance အရောင်း agent** တွေအတွက် product knowledge assistant တစ်ခုပါ။

Hackathon challenge က —

> Reimagining Customer Engagement Through AI-Powered Digital Assistants

### ဖြေရှင်းချင်တဲ့ ပြဿနာ

Agent တစ်ယောက်က customer နဲ့ စကားပြောနေတဲ့အခါ product အကြောင်း အမြန်၊ အတိအကျ သိရမယ်။ ဒါပေမယ့် လက်တွေ့မှာ အချက်အလက်တွေက —

- brochure
- policy document
- benefit table
- guide
- FAQ
- training material

စတဲ့ နေရာမျိုးစုံမှာ ကွဲပြားနေတယ်။ ဒါကြောင့် ရှာရတာ နှေးတယ်။ ပိုအရေးကြီးတာက agent တစ်ယောက်နဲ့ တစ်ယောက် customer ကို ပြောတဲ့အဖြေ မတူဘဲ ဖြစ်နိုင်တယ်။

### ကျွန်တော်တို့ ဖြေရှင်းပုံ

Agent က သဘာဝဘာသာစကားနဲ့ မေးခွန်းတစ်ခု မေးလိုက်တယ်။ InsureAssist က **ခွင့်ပြုထားတဲ့ document ထဲက** အဖြေကို ရှင်းလင်းစွာ ပြန်ပေးတယ်။ အဲဒီအဖြေနဲ့အတူ အရေးကြီးတဲ့ သတ်မှတ်ချက် (conditions)၊ ချွင်းချက် (exclusions) နဲ့ **ဘယ် document ဘယ် section ကလာတာလဲ** ဆိုတဲ့ source ကိုပါ တွဲပြပေးတယ်။

---

## ၂။ အဓိက flow (core journey)

```text
Agent က InsureAssist ကို ဖွင့်တယ်
        ↓
Product ရွေးတယ် / မေးခွန်းမေးတယ်
        ↓
ခွင့်ပြုထားတဲ့ product အချက်အလက်ကို ရှာယူတယ် (retrieval)
        ↓
အဖြေ ပြတယ်
        ↓
အရေးကြီးတဲ့ conditions / exclusions ကို သီးသန့် ထုတ်ပြတယ်
        ↓
Source ကိုးကားချက် ပြတယ်
        ↓
(optional) n8n နဲ့ follow-up action ဖန်တီးတယ်
```

နောက်ဆုံး step က **optional** ပါ။ အဓိက flow အရင် အလုပ်လုပ်ရမယ်။

### နမူနာ

Agent မေးတယ် —

> Product A မှာ ဆေးရုံတက်ခ benefit ဘယ်လောက်ရလဲ

InsureAssist ပြန်ဖြေတယ် —

- ရှင်းလင်းတဲ့ အဖြေ
- benefit ပမာဏ
- ကန့်သတ်ချက် (limitation)
- သက်ဆိုင်တဲ့ condition
- Source: Product A Brochure, Hospital Benefits section

---

## ၃။ System architecture — ဘယ်အပိုင်းက ဘာတာဝန်ယူလဲ

```text
                  အရောင်း AGENT
                       │
                       ▼
                  Next.js Web
                  + Tailwind
                       │
                     HTTPS
                       │
                       ▼
                    FastAPI
                       │
             ┌─────────┼──────────┐
             ▼         ▼          ▼
          Product   Knowledge    n8n
          Service   Retrieval  (optional)
                       │
                       ▼
                    LLM API
                       │
                       ▼
              Grounded Answer
                  + Sources
```

| အပိုင်း | တာဝန် |
| --- | --- |
| `apps/web/` (Next.js) | Agent မြင်တဲ့ UI။ Document ထားထားတဲ့ API ကိုပဲ ခေါ်တယ် |
| `services/api/` (FastAPI) | Validation, product logic, retrieval, prompt, AI ခေါ်ဆိုမှု, secret အားလုံး |
| LLM | ရှာယူထားတဲ့ အချက်အလက်ကနေ အဖြေ ရေးပေးတယ် |
| n8n | Follow-up email / reminder သာ။ Product knowledge logic **မထားရ** |

### အရေးကြီးတဲ့ စည်းမျဉ်း

**Browser (frontend) ကနေ LLM ကို တိုက်ရိုက် မခေါ်ရဘူး။** API key အားလုံး FastAPI ဆီမှာပဲ ရှိရမယ်။ n8n webhook URL လည်း အတူတူပါ — server side မှာပဲ ထားရမယ်။

ဒါက `docs/SECURITY.md` ထဲမှာ ရေးထားတဲ့ စည်းမျဉ်းပါ။

---

## ၄။ Grounded answer ဆိုတာ ဘာလဲ

ဒီ project ရဲ့ အသက်ပါ။ ကောင်းကောင်း နားလည်ထားရမယ်။

**Grounded answer** ဆိုတာ အဖြေတိုင်းက ခွင့်ပြုထားတဲ့ product document ထဲကနေ လာရမယ် ဆိုတာပါ။ AI က ကိုယ်တိုင် သိထားတဲ့ အထွေထွေ insurance အသိပညာနဲ့ ထင်ကြေးပေး **မဖြေရဘူး**။

ဒါကြောင့် လိုက်နာရမယ့် အချက်တွေ —

- အဖြေက ခွင့်ပြုထားတဲ့ document ကနေပဲ လာရမယ်
- ဖြစ်နိုင်သလောက် ဘယ် document ဘယ် section လဲ ကိုးကားပြရမယ်
- သက်ဆိုင်တဲ့ condition နဲ့ exclusion ကို ချန်လှပ်ခြင်း **မလုပ်ရဘူး**
- Document မှာ မပါတဲ့ အချက်ကို **လုံးဝ လုပ်ကြံ မရေးရဘူး**
- မသိရင် "ဒီအချက်အလက် မရရှိနိုင်ပါ" လို့ ရိုးရိုးသားသား ပြောရမယ်၊ ပြီးတော့ ဘယ် source လိုအပ်လဲ ဆိုတာ ထောက်ပြရမယ်

Benefit ပမာဏ၊ ကန့်သတ်ချက်၊ eligibility rule၊ exclusion၊ coverage condition — ဒါတွေကို လုပ်ကြံရေးလိုက်ရင် insurance product မှာ တကယ့် အမှား ဖြစ်စေတယ်။ ဒါကြောင့် ဒီစည်းမျဉ်းက တင်းကြပ်ပါတယ်။

အသေးစိတ်ကို `docs/KNOWLEDGE_STRATEGY.md` မှာ ကြည့်ပါ။

---

## ၅။ n8n automation အပိုင်း

n8n က **အဓိက AI အလုပ်ကို မလုပ်ဘူး**။ FastAPI က အဖြေထုတ်ပြီးသားကို ယူပြီး လက်တွေ့ action အဖြစ် ပြောင်းပေးတာပဲ လုပ်တယ်။

```text
Grounded အဖြေ ရပြီး
        ↓
Agent က follow-up ခလုတ် နှိပ်တယ်
        ↓
FastAPI → n8n webhook
        ↓
Agent ရဲ့ email ထဲ draft ရောက်တယ်
```

### Workflow ၂ မျိုး

**Workflow 1 — Follow-up draft** (အဓိက၊ demo အတွက်)

Agent ရလိုက်တဲ့ grounded အဖြေကို customer ဆီ ပြန်ပို့နိုင်တဲ့ စာ draft အဖြစ် **agent ကိုယ်တိုင်ရဲ့ email** ဆီ ပို့ပေးတယ်။

Customer ရဲ့ email ကို **မယူဘူး**။ ဘာလို့လဲ ဆိုတော့ demo မှာ customer PII (personal information) မသုံးရ ဆိုတဲ့ စည်းမျဉ်း ရှိတယ်။ ဒါကြောင့် agent ဆီ draft ပို့ပေးပြီး agent ကိုယ်တိုင် forward လုပ်တဲ့ ပုံစံက scope အတွင်းမှာ ရှိတယ်။

ဒီ workflow မှာ IF node တစ်ခု ပါတယ်။ `confidence` က `grounded` မဟုတ်ရင် email **မပို့ဘူး**။ Ground မဖြစ်တဲ့ အဖြေကို customer ဆီ ပို့လို့ရတဲ့ စာအဖြစ် ပြောင်းလိုက်တာ မှားတယ်။ ဒါကြောင့် ငြင်းပယ်တာက ဆော့ဖ်ဝဲ အမှား မဟုတ်ဘူး — မှန်ကန်တဲ့ အလုပ်လုပ်ပုံပါ။

**Workflow 2 — Knowledge gap escalation** (optional)

မေးခွန်းကို ခွင့်ပြုထားတဲ့ document တွေနဲ့ မဖြေနိုင်တဲ့အခါ အဲဒီ gap ကို document ထိန်းသိမ်းတဲ့ သူဆီ အသိပေးတယ်။ "မသိဘူး" လို့ ပြောပြီး ပြီးသွားတာ မဟုတ်ဘဲ လိုအပ်တဲ့ source ကို တောင်းဆိုတဲ့ action အဖြစ် ပြောင်းပေးတယ်။

ဒါက အချိန်ရရင်သာ လုပ်ရမယ့် အပိုင်းပါ။

အသေးစိတ်ကို `docs/N8N_WORKFLOW.md` မှာ ကြည့်ပါ။

---

## ၆။ လက်ရှိ code အခြေအနေ

**အရေးကြီးတယ်** — အခု repository မှာ foundation ပဲ ရှိတယ်။ Feature တွေ မရေးရသေးဘူး။

```text
insurance_product_knowledge_assistant/
├── AGENTS.md
├── README.md
├── .cursor/rules/          ← Cursor rule များ
├── docs/                   ← spec / contract / စည်းမျဉ်း
├── apps/web/               ← Next.js scaffold (run လို့ရတယ်)
└── services/api/           ← FastAPI scaffold (run လို့ရတယ်)
```

အခု အလုပ်လုပ်တာ —

- `GET /api/v1/health` တစ်ခုပဲ implement ထားတယ်
- Next.js scaffold က build လုပ်လို့ရတယ်
- FastAPI scaffold က test pass တယ်

အခု **မရှိသေးတာ** —

- AI ခေါ်ဆိုမှု
- retrieval / RAG / embeddings
- document upload / PDF extraction
- question answering endpoint
- product comparison
- n8n workflow ခေါ်တဲ့ backend code
- database / authentication

`POST /api/v1/assistant/ask` က `docs/API_CONTRACT.md` မှာ **PLANNED** လို့ ရေးထားတယ်။ ဒါကို ရှိပြီးသား endpoint လို မမှတ်ရဘူး။ Document ထဲက နမူနာ တစ်ခု ရှိနေတာက အဲဒါကို implement လုပ်ခွင့် ရပြီး ဆိုတာ မဟုတ်ဘူး။

---

## ၇။ API contract နဲ့ စည်းမျဉ်း

Base path — `/api/v1`

| Endpoint | အခြေအနေ |
| --- | --- |
| `GET /api/v1/health` | IMPLEMENTED |
| `POST /api/v1/assistant/ask` | PLANNED |
| `POST /api/v1/assistant/compare` | PLANNED (schema မတည်သေး) |

### API ပြောင်းချင်ရင် လိုက်နာရမယ့် အစီအစဉ်

Endpoint path, HTTP method, field name, field type, response ပုံစံ — ဒါတွေကို **တစ်ယောက်တည်း သဘောနဲ့ မပြောင်းရဘူး**။

1. Integration Lead (Developer 4) နဲ့ တိုင်ပင်တယ်
2. `docs/API_CONTRACT.md` ကို update လုပ်တယ်
3. Backend ပြောင်းတယ်
4. Frontend ပြောင်းတယ်
5. Integration test လုပ်တယ်
6. ရှင်းလင်းတဲ့ commit message နဲ့ commit တယ်

ဒီအစီအစဉ်ကို မလိုက်နာရင် web နဲ့ api နှစ်ဖက် ကွဲပြီး integration အချိန်မှာ ပြဿနာ တင်တယ်။

---

## ၈။ Team ၄ ယောက် တာဝန်ခွဲမှု

Merge conflict မဖြစ်စေရန် နယ်ပယ် ခွဲထားတာပါ။ Contract ကို တစ်ယောက်တည်း ပြောင်းခွင့် ရတာ မဟုတ်ဘူး။

**Developer 1 — Web Frontend**
`apps/web/**` ကို ပိုင်တယ်။ Agent dashboard, product selector, မေးခွန်း UI, အဖြေနဲ့ source ပြသမှု, loading / error state တွေ။ Secret နဲ့ AI ခေါ်ဆိုမှုကို browser ထဲ **မထားရ**။

**Developer 2 — Backend / API**
`services/api/**` ကို ပိုင်တယ်။ FastAPI endpoint, validation, schema, error ပုံစံ, document / product service, retrieval integration။

**Developer 3 — AI / Knowledge / Automation**
AI integration, prompt engineering, retrieval, answer grounding နဲ့ citation, n8n automation။ အနာဂတ်မှာ `services/api/app/services/ai/`, `knowledge/`, `automation/` အောက်မှာ အလုပ်လုပ်တယ်။

**Developer 4 — Integration / Deployment**
Git integration, PR review, API contract ချိန်ညှိမှု, environment config, deployment, end-to-end test, demo ပြင်ဆင်မှု, scope ထိန်းချုပ်မှု။ Feature ကြီးတစ်ခု တစ်ယောက်တည်း **မယူရ**။ သူ့အဓိက တာဝန်က demo တစ်ခုလုံး အလုပ်လုပ်စေရန်နဲ့ `main` ကို အမြဲ run လို့ရနေစေရန်ပါ။

Developer 2 နဲ့ 3 က backend ထဲ shared code ပြောင်းရင် အရင် ညှိရမယ်။

---

## ၉။ ၄ နာရီ အချိန်စီစဉ်မှု

| အချိန် | လုပ်ရမယ့်အလုပ် |
| --- | --- |
| 00:00–00:20 | Scope, ownership, contract, document set အတည်ပြု |
| 00:20–01:40 | ကိုယ်စီ branch မှာ တစ်ပြိုင်နက် feature ရေး |
| 01:40–02:00 | ပထမဆုံး integration |
| **02:00** | **End-to-end MVP အလုပ်လုပ်ရမယ်** |
| 02:00–02:45 | အဖြေအရည်အသွေး နဲ့ UX ကောင်းလာစေရန် |
| 02:45–03:15 | Deploy, environment စစ်, error ဖြေရှင်း |
| **03:15** | **Feature freeze** |
| 03:15–03:40 | Demo polish |
| 03:40–04:00 | Demo လေ့ကျင့်ခြင်း |

### အရေးကြီးဆုံး စည်းမျဉ်း

၂ နာရီ အချိန်မှာ ဒီ flow အလုပ်မလုပ်ရင် —

```text
မေးခွန်း → knowledge retrieval → grounded အဖြေ → source
```

optional အလုပ် အားလုံး ရပ်ပြီး team တစ်ခုလုံး ဒီ core flow ကိုပဲ ပြင်ရမယ်။ n8n, comparison, voice အားလုံး ခဏ ဘေးဖယ်ထားရမယ်။

---

## ၁၀။ Scope ပြင်ပ — မလုပ်ရမယ့် အရာများ

ဒါတွေ ထည့်ချင်စိတ် ပေါ်လာနိုင်တယ်။ ဒါပေမယ့် `docs/PRODUCT_SCOPE.md` အရ **out of scope** ပါ။

- Customer ကို တိုက်ရိုက် ဖြေတဲ့ chatbot
- Claims
- Underwriting
- Quotation / premium တွက်ချက်မှု
- Policy ထုတ်ပေးမှု
- Payment
- CRM / lead management
- Authentication
- Document management system အပြည့်အစုံ
- Enterprise search platform
- ကိုယ်တိုင် ဆုံးဖြတ်တဲ့ autonomous sales agent

Architecture diagram, API နမူနာ, UI scaffold တွေ ရှိနေတာက အဲဒီ feature တွေ လုပ်ခွင့် ရပြီး ဆိုတာ မဟုတ်ဘူး။

---

## ၁၁။ Demo ပြသမယ့် ပုံစံ

### အဓိက scenario

Agent မေးတယ် —

> Product A မှာ ဆေးရုံတက်ခ benefit ဘယ်လိုရလဲ

ပြရမယ့်အချက် —

1. နားလည်လွယ်တဲ့ အဖြေ
2. သက်ဆိုင်တဲ့ limitation / condition
3. Source ကိုးကားချက် (Product A Brochure, Hospital Benefits section)

### နောက်ဆက်တွဲ (အချိန်ရရင်)

- Product နှစ်ခု နှိုင်းယှဉ်ပြခြင်း
- n8n follow-up draft ပို့ပြခြင်း
- မဖြေနိုင်တဲ့ မေးခွန်းကို ရိုးသားစွာ "မရရှိနိုင်ပါ" ပြောပြခြင်း

နောက်ဆုံးအချက်က အထင်မထားလောက်ဘဲ အမှတ်ကောင်းရတယ်။ AI က လုပ်ကြံမဖြေဘဲ ရိုးသားစွာ ငြင်းတာကို ပြနိုင်တာက insurance domain မှာ ယုံကြည်စိတ်ချရမှု ရှိတယ် ဆိုတာ သက်သေပြတယ်။

### Demo သတိထားရမယ့်အချက်

- Customer PII လုံးဝ မသုံးရ
- ကိုးကားမယ့် document section ကို အရင် အတည်ပြုထားရမယ်
- Document မှာ မပါတဲ့ အချက်ကို အာဏာရှိတဲ့ policy အဖြေလို မပြောရ
- Mock data ကို live AI အဖြေလို ဟန်ဆောင် **မပြရဘူး**
- Feature freeze ပြီးနောက် တည်မငြိမ်တဲ့ optional feature မပြရ

---

## ၁၂။ Local မှာ run ဖို့

### Backend

```bash
cd services/api
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API — `http://localhost:8000`
- Health — `http://localhost:8000/api/v1/health`
- Swagger — `http://localhost:8000/docs`

### Web

```bash
cd apps/web
npm install
npm run dev
```

- Web — `http://localhost:3000`

### Environment

`.env.example` ကိုပဲ commit တယ်။ တကယ့် `.env` ကို **လုံးဝ မ commit ရဘူး**။

- `apps/web/.env.example` → `NEXT_PUBLIC_API_BASE_URL`
- `services/api/.env.example` → `APP_ENV`, `CORS_ORIGINS`

`NEXT_PUBLIC_*` က browser မှာ မြင်တယ်။ ဒါကြောင့် secret **မထားရ**။

AI key, n8n webhook URL တွေက backend deployment environment မှာပဲ ရှိရမယ်။

---

## ၁၃။ Git အလုပ်လုပ်ပုံ

Branch —

```text
main
feature/web-*
feature/api-*
feature/knowledge-*
feature/integration-*
```

- `main` ပေါ်မှာ တိုက်ရိုက် မရေးရ
- Commit အသေးအသေး မကြာခဏ လုပ်
- PR အသေး ထား
- သူတစ်ပါး ownership နယ်ပယ်ကို မထိ
- API contract ပြောင်းရင် အရင် ညှိ
- `main` က အမြဲ demo ပြလို့ရနေရမယ်

Commit နမူနာ —

```text
feat(web): add product question interface
feat(api): add assistant ask endpoint
docs(api): update ask response contract
fix(api): validate empty question
```

---

## အကျဉ်းချုပ်

```text
Agent မေးခွန်း
     ↓
FastAPI (validation + retrieval)
     ↓
ခွင့်ပြုထားတဲ့ document ထဲက အချက်အလက်
     ↓
LLM → grounded အဖြေ + condition + source
     ↓
Next.js မှာ ပြသ
     ↓
(optional) n8n → follow-up draft
```

မှတ်ထားရမယ့် အချက် ၃ ချက် —

1. **အဖြေတိုင်း document ကနေ လာရမယ်။** လုပ်ကြံ မရေးရဘူး။
2. **Secret အားလုံး backend မှာ။** Browser ထဲ မထားရ။
3. **၂ နာရီမှာ core flow အလုပ်လုပ်ရမယ်။** မလုပ်ရင် အားလုံး ရပ်ပြီး ဒါကိုပဲ ပြင်ရမယ်။
