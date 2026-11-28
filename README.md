> Giờ, mốc, luật, rubric: xem `README.md`, `02-guide.md`, `03-rubric.md` trong repo đề (bộ đề BTC phát).

# F4VSB — Đánh giá rủi ro SMS ngân hàng và ví điện tử

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = phần nhỏ nhất làm xong được trong hackathon: một người dùng · một việc · một quyết định AI · một kết quả.*

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Ví dụ track A (ví dụ cỡ, không phải lời giải):* nhóm viết công cụ `search_lesson` tra bài pre-class đã đánh mã đoạn, luồng "tra đoạn → model trả lời kèm mã đoạn, không có thì nói không có", metric "mọi khẳng định có mã đoạn đúng", persona "ôn dồn trước kiểm tra". Khung chạy 25 câu thử ra `run-1.csv`, nhóm chấm `pass`, `score` in % đạt; `simulate` chạy 50 phiên ra chi phí / task thành công cho hai model.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- `python run.py` in ra "[câu trả lời giả — chưa nối model] …" là khung chạy đúng. Nối model thật: [docs/connect-model.md](docs/connect-model.md).

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Giao diện web Next.js

Cần Node.js 20.9 trở lên và Python 3.10 trở lên. Từ gốc repo, chạy:

```powershell
cd web
npm ci
npm run dev
```

Mở `http://127.0.0.1:3000`, dán một SMS hoặc chọn tin nhắn mẫu, rồi bấm **Kiểm tra SMS**. Web gọi cùng luồng `answer()` như CLI. Python đọc cấu hình DeepSeek từ `.env` ở gốc repo. Khi chưa có cấu hình model, trang hiển thị rõ kết quả chế độ giả.

Nếu Python không nằm trên `PATH`, đặt `PYTHON_BIN` thành đường dẫn tuyệt đối tới trình chạy Python. Web mặc định dùng `python` trên Windows và `python3` trên macOS/Linux. Để chạy bản build, dùng `npm run build` rồi `npm start` trong `web/`. Máy chạy web cần có cả Node.js, Python và các thư mục `codebase/`, `data/` của repo.

### Deploy bằng Docker Compose và Cloudflare Tunnel

Chạy từ gốc repo dưới user `proj2` trên VPS. Cần Docker rootless và Docker Compose từ 2.24. Khi chưa có `.env.deploy`, ứng dụng chạy ở chế độ giả.

```bash
docker compose up -d --build --wait
docker compose ps
docker compose exec -T app node -e "fetch('http://127.0.0.1:8080/health').then(r=>r.text()).then(console.log)"
```

Trong Cloudflare Tunnel, cấu hình hostname `kiemtrasms.online` với service `http://app:8080`. Khi chuyển địa chỉ web sang tunnel, thay các bản ghi A của trang đỗ GoDaddy ở tên miền gốc bằng bản ghi do tunnel tạo. App nhận lưu lượng từ tunnel qua mạng Compose nội bộ.

Chạy `umask 077` trước khi tạo file cấu hình trên VPS. Tạo `.env.tunnel` với dòng `TUNNEL_TOKEN=` và điền token tunnel. Khi bật DeepSeek, sao chép `.env.example` thành `.env.deploy` và điền cấu hình model thật. Kiểm tra quyền của hai file là `600`.

```bash
docker compose --profile tunnel up -d --build --wait
docker compose --profile tunnel logs --tail 50 tunnel
curl -fsS https://kiemtrasms.online/health
```

Bật giới hạn request cho `/api/analyze` trên Cloudflare trước khi chạy DeepSeek thật. Sau khi deploy, mở trang trên tên miền và kiểm tra một SMS mẫu trên giao diện.

### Cập nhật qua GitHub

1. Làm việc trên nhánh riêng rồi mở pull request vào `main`. Chờ kiểm tra **CI** qua trước khi merge.
2. Muốn lên VPS, mở pull request từ `main` vào `deloy`. Chờ **CI** qua rồi merge.
3. VPS kiểm tra nhánh `deloy` khoảng mỗi phút. Khi **CI** trên chính commit mới đã qua, VPS build image và cập nhật container web. Nếu bản mới khởi động lỗi, VPS thử khôi phục container trước đó.

Xem lần deploy gần nhất bằng `journalctl --user -u f4vsb-deploy.service -n 30` dưới user `proj2`. Sau đó mở `https://kiemtrasms.online/health` để kiểm tra. Cấu hình DeepSeek và Cloudflare được lưu trong `~/f4vsb` trên VPS.

Khi cài quy trình lần đầu trên VPS đã chạy F4VSB, sao chép `deploy/deploy.sh` vào `~/f4vsb/bin/` và hai tệp systemd vào `~/.config/systemd/user/`. Chạy `systemctl --user daemon-reload` rồi `systemctl --user enable --now f4vsb-deploy.timer`. Cập nhật các tệp tương ứng trên VPS nếu sửa quy trình deploy.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên (làm trước CP3) → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng chính, đúng hình dạng ở `spec.md` §4. Khung có sẵn một workflow 2 bước *ví dụ* | 3.2 |
| `codebase/tools.py` | Công cụ của bài toán, mỗi công cụ một hàm có `@tool` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model. Chưa điền `.env` thì chạy **chế độ giả** | 3.3 |

- **Trước CP2:** để chế độ giả, công cụ trả dữ liệu giả — `python run.py` đi hết luồng là đủ.
- **Model thật:** điền key DeepSeek trong `.env` theo [hướng dẫn kết nối](docs/connect-model.md), chạy `python run.py eval --try` để xác nhận token > 0 rồi chạy `python run.py eval`.
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (bài học, thông báo, lịch…) để trong `data/`, đọc qua công cụ.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | **Thật** khi cấu hình `.env` | `deepseek-flash` phân loại theo tín hiệu đã kiểm (chưa có `.env` thì fallback chế độ `fake`). |
| Danh bạ kênh chính thức & quy tắc SMS | **Thật** (cục bộ) | 10 ngân hàng/ví công khai trong `data/official_channels.json` và bộ quy tắc trong `data/domain_rules.json`. |
| Truy cập hộp thư SMS / thao tác tài khoản | **Không làm** | Ngoài lát cắt; người dùng tự dán SMS đã ẩn danh và tự xác minh qua app/kênh chính thức. |

## Dùng AI vào việc gì

2–3 dòng (bắt buộc): nhóm dùng công cụ AI nào để làm gì, người kiểm lại phần nào. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md). Coding agent đọc [AGENTS.md](AGENTS.md).

Codex hỗ trợ tích hợp API DeepSeek, sửa hướng dẫn chạy và đề xuất điểm lượt 1 dựa trên 20 đầu ra thật. Đăng đã rà cột `pass` và xác nhận giữ kết quả 19/20.

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | [Slide CP4](demo-slides.pdf), [kịch bản demo](slides/outline.md) và [video DeepSeek CP3 có thể mở khi cần dự phòng](https://drive.google.com/file/d/1phQP125iCu62ZdLdCvC_aVFa5QX8Kb2A/view?usp=sharing). Video CP3 sử dụng kết quả lượt 1. |
| + | *Bonus:* người dùng thử | `validation/log.md` |
