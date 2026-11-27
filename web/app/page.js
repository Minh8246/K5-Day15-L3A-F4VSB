import SmsCheck from "./sms-check";

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#noi-dung">Đến nội dung chính</a>
      <header className="site-header">
        <div className="container header-row">
          <a className="brand" href="#dau-trang" aria-label="F4VSB, về đầu trang">
            <span className="brand-mark" aria-hidden="true"><span /></span>
            <span>F4VSB</span>
          </a>
          <nav className="header-nav" aria-label="Điều hướng trang">
            <a href="#huong-dan">Cách dùng</a>
            <a href="#tu-xac-minh">Tự xác minh</a>
          </nav>
          <a className="check-link header-action" href="#kiem-tra">Kiểm tra SMS <span aria-hidden="true">↓</span></a>
        </div>
      </header>

      <main id="noi-dung" tabIndex={-1}>
        <section className="hero" id="dau-trang" aria-labelledby="hero-title">
          <div className="container hero-inner">
            <div className="hero-copy">
              <h1 id="hero-title">Kiểm tra SMS<br /> <span>trước khi làm theo.</span></h1>
              <p>Đối chiếu tin nhắn ngân hàng hoặc ví điện tử để nhận biết dấu hiệu lừa đảo và tìm kênh xác minh.</p>
              <div className="hero-actions">
                <a className="check-link" href="#kiem-tra">Kiểm tra ngay <span aria-hidden="true">↓</span></a>
                <a className="scroll-link" href="#huong-dan">
                  <span className="scroll-icon" aria-hidden="true" />
                  Tìm hiểu cách dùng
                </a>
              </div>
            </div>
            <div className="hero-art" aria-hidden="true">
              <div className="art-grid" />
              <div className="orbit orbit-outer" />
              <div className="orbit orbit-middle" />
              <div className="orbit orbit-inner" />
              <div className="radar-sweep" />
              <i className="signal signal-one" /><i className="signal signal-two" />
              <div className="signal-card">
                <div className="signal-bubble"><i /><i /><i /></div>
                <div className="signal-lines"><span /><span /><span /></div>
                <i className="signal-check" />
              </div>
            </div>
          </div>
        </section>

        <section className="page-section" id="kiem-tra" aria-labelledby="check-title">
          <div className="container">
            <h2 className="section-title" id="check-title">Kiểm tra một tin nhắn</h2>
            <SmsCheck />
          </div>
        </section>

        <section className="page-section guide-section" id="huong-dan" aria-labelledby="guide-title">
          <div className="container">
            <h2 className="section-title" id="guide-title">Cách dùng</h2>
            <ol className="guide-steps">
              <li>
                <h3>Dán nội dung SMS</h3>
                <p>Che mã OTP, số tài khoản và thông tin cá nhân. Giữ lại lời yêu cầu và tên miền để đối chiếu.</p>
              </li>
              <li>
                <h3>Đọc lý do cảnh báo</h3>
                <p>Kết quả nêu dấu hiệu rủi ro phát hiện được hoặc cho biết dữ liệu còn thiếu.</p>
              </li>
              <li>
                <h3>Xem cách tự xác minh</h3>
                <p>Dùng mục Tự xác minh trong kết quả để tìm kênh liên hệ phù hợp trước khi làm theo yêu cầu.</p>
              </li>
            </ol>
          </div>
        </section>

        <section className="page-section verify-section" id="tu-xac-minh" aria-labelledby="verify-title">
          <div className="container verify-inner">
            <h2 className="section-title" id="verify-title">Gặp SMS đáng ngờ?</h2>
            <ul className="verify-list">
              <li>Dừng thao tác và tránh mở liên kết trong tin nhắn.</li>
              <li>Tự mở ứng dụng ngân hàng hoặc ví điện tử để kiểm tra tài khoản.</li>
              <li>Tìm số tổng đài ở mục hỗ trợ trong ứng dụng hoặc trên website chính thức.</li>
            </ul>
          </div>
        </section>
      </main>

      <footer className="container footer-row">
        <span><strong>F4VSB</strong> <span className="footer-separator">/</span> AI20K K5</span>
        <div className="footer-links">
          <a href="https://github.com/Minh8246/K5-Day15-L3A-F4VSB" target="_blank" rel="noreferrer">Mã nguồn GitHub <span aria-hidden="true">↗</span></a>
          <a href="#dau-trang">Về đầu trang <span aria-hidden="true">↑</span></a>
        </div>
      </footer>
    </>
  );
}
