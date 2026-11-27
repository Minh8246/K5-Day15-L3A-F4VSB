import { execFile } from "node:child_process";
import path from "node:path";
import { MAX_SMS_LENGTH } from "../../../lib/sms";

export const runtime = "nodejs";

function analyze(message) {
  const python = process.env.PYTHON_BIN || (process.platform === "win32" ? "python" : "python3");
  const script = path.join(process.cwd(), "analyze_sms.py");

  return new Promise((resolve, reject) => {
    const child = execFile(/* turbopackIgnore: true */ python, [script], {
      env: { ...process.env, PYTHONIOENCODING: "utf-8" },
      encoding: "utf8",
      timeout: 35_000,
      maxBuffer: 128 * 1024,
      windowsHide: true,
    }, (error, stdout) => {
      if (error) {
        reject(error);
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch (parseError) {
        reject(parseError);
      }
    });
    child.stdin.on("error", reject);
    child.stdin.end(JSON.stringify({ message }), "utf8");
  });
}

export async function POST(request) {
  const origin = request.headers.get("origin");
  const host = request.headers.get("host");
  if (origin && origin !== `http://${host}` && origin !== `https://${host}`) {
    return Response.json({ error: "Yêu cầu phải được gửi từ trang kiểm tra SMS." }, { status: 403 });
  }
  if (request.headers.get("content-type")?.split(";")[0].trim().toLowerCase() !== "application/json") {
    return Response.json({ error: "Định dạng yêu cầu không hợp lệ." }, { status: 415 });
  }

  let payload;
  try {
    payload = await request.json();
  } catch {
    return Response.json({ error: "Không đọc được nội dung yêu cầu." }, { status: 400 });
  }

  if (typeof payload?.message !== "string" || !payload.message.trim()) {
    return Response.json({ error: "Hãy nhập nội dung SMS để kiểm tra." }, { status: 400 });
  }
  if (payload.message.length > MAX_SMS_LENGTH) {
    return Response.json({ error: `Nội dung SMS tối đa ${MAX_SMS_LENGTH} ký tự.` }, { status: 400 });
  }

  try {
    const result = await analyze(payload.message.trim());
    return Response.json(result, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return Response.json({ error: "Chưa thể phân tích lúc này. Hãy kiểm tra cấu hình Python, DeepSeek và thử lại." }, { status: 502 });
  }
}
