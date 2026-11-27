"use client";

import { useRef, useState } from "react";
import { MAX_SMS_LENGTH } from "../lib/sms";

const examples = [
  { name: "Tên miền lạ", message: "Vietcombank: Vui lòng xác minh tài khoản tại https://xacminh.example.invalid." },
  { name: "Đòi mã OTP", message: "MoMo: Vui lòng gửi mã OTP để mở khóa tài khoản." },
  { name: "Khuyến cáo bảo mật", message: "Vietcombank khuyến cáo: Không cung cấp OTP cho bất kỳ ai." },
];

export default function SmsCheck() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const input = useRef(null);

  function updateMessage(value) {
    setMessage(value);
    setResult(null);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (pending || !message.trim()) return;

    setPending(true);
    setResult(null);
    setError("");
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      if (response.ok) setResult(data);
      else setError(data.error || "Không phân tích được tin nhắn. Hãy thử lại.");
    } catch {
      setError("Không kết nối được dịch vụ phân tích. Hãy thử lại.");
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="container workspace">
      <form className="panel input-panel" onSubmit={handleSubmit} aria-labelledby="input-title">
        <div className="panel-heading">
          <h2 id="input-title">Tin nhắn cần kiểm tra</h2>
          <button className="reset-button" type="button" disabled={!message || pending} onClick={() => {
            updateMessage("");
            input.current?.focus();
          }}>Xóa nội dung</button>
        </div>
        <label className="sr-only" htmlFor="sms-message">Nội dung SMS</label>
        <div className="composer">
          <textarea id="sms-message" ref={input} placeholder="Dán nội dung SMS vào đây…" value={message}
            maxLength={MAX_SMS_LENGTH} disabled={pending} onChange={(event) => updateMessage(event.target.value)}
            aria-describedby="sms-privacy" required />
          <div className="counter" aria-label={`${message.length} trên ${MAX_SMS_LENGTH} ký tự`}>{message.length} / {MAX_SMS_LENGTH}</div>
        </div>

        <div className="examples" aria-label="Tin nhắn mẫu">
          <span>Thử với</span>
          {examples.map((example) => (
            <button type="button" key={example.name} disabled={pending} onClick={() => updateMessage(example.message)}>
              {example.name}
            </button>
          ))}
        </div>

        <div className="form-actions">
          <p id="sms-privacy"><span className="lock-mark" aria-hidden="true" /> Che OTP, số tài khoản và thông tin cá nhân trước khi dán.</p>
          <button className="submit-button" type="submit" disabled={pending || !message.trim()}>
            {pending ? "Đang kiểm tra…" : "Kiểm tra SMS"} <span aria-hidden="true">→</span>
          </button>
        </div>
      </form>

      <section className="panel result-panel" aria-labelledby="result-title" aria-busy={pending}>
        <div className="panel-heading"><h2 id="result-title">Kết quả phân tích</h2></div>
        <div className="result-content" aria-live="polite">
          {pending ? (
            <div className="empty-state">
              <span className="state-icon spinner" aria-hidden="true" />
              <p className="state-title">Đang kiểm tra tín hiệu</p>
              <p>Đối chiếu nội dung với quy tắc và danh bạ.</p>
            </div>
          ) : error ? (
            <div className="empty-state error-state" role="alert">
              <span className="state-icon" aria-hidden="true">!</span>
              <p className="state-title">Phân tích gián đoạn</p>
              <p>{error}</p>
            </div>
          ) : result ? (
            <div className="filled-result">
              <div className={`result-label ${result.risk}`}><span aria-hidden="true">{result.risk === "high" ? "!" : "?"}</span>{result.label}</div>
              {result.model === "fake" && <p className="mock-note">Chế độ giả · Chưa gọi DeepSeek.</p>}
              <h3>Lý do</h3><p>{result.reason}</p>
              {result.organization && <>
                <h3>Danh bạ đối chiếu</h3>
                <p>{result.source ? <a className="directory-link" href={result.source} target="_blank" rel="noreferrer">
                  {result.organization} <span aria-hidden="true">↗</span>
                </a> : result.organization}</p>
              </>}
              <h3>Tự xác minh</h3><p>{result.guidance}</p>
              {result.model && result.model !== "fake" && <div className="model-meta">{result.model} <span>·</span> {result.tokensIn} token vào / {result.tokensOut} ra</div>}
            </div>
          ) : (
            <div className="empty-state">
              <span className="state-icon" aria-hidden="true"><span className="scan-mark" /></span>
              <p className="state-title">Chưa có kết quả</p>
              <p>Dán SMS hoặc chọn một tin nhắn mẫu để bắt đầu.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
