import "./globals.css";

export const metadata = {
  title: "F4VSB — Kiểm tra rủi ro SMS",
  description: "Đối chiếu SMS ngân hàng và ví điện tử để nhận diện dấu hiệu rủi ro và tìm cách tự xác minh.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
