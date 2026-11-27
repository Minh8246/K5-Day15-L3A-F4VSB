export default function Home() {
  return (
    <>
      <header className="site-header">
        <div className="container header-row">
          <a className="brand" href="/" aria-label="F4VSB, trang chủ">
            <span className="brand-mark" aria-hidden="true"><span /></span>
            <span>F4VSB</span>
          </a>
          <span className="header-caption">Kiểm tra SMS ngân hàng &amp; ví điện tử</span>
        </div>
      </header>

      <main>
        <section className="hero" aria-labelledby="hero-title">
          <div className="container hero-inner">
            <div className="hero-copy">
              <h1 id="hero-title">Kiểm tra SMS<br /> <span>trước khi làm theo.</span></h1>
              <p>Dán tin nhắn để xem dấu hiệu đáng ngờ và tìm cách xác minh qua kênh chính thức.</p>
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

      </main>

      <footer className="container footer-row">
        <span><strong>F4VSB</strong> <span className="footer-separator">/</span> AI20K K5</span>
        <a href="https://github.com/Minh8246/K5-Day15-L3A-F4VSB" target="_blank" rel="noreferrer">Mã nguồn GitHub <span aria-hidden="true">↗</span></a>
      </footer>
    </>
  );
}
